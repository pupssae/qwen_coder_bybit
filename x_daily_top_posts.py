#!/usr/bin/env python3
"""
X Daily Top Posts - Find the most popular posts from specified accounts in the last 24 hours.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text


# List of accounts to monitor
ACCOUNTS = [
    "LG_AI_Research",
    "bridgemindai",
    "MiniMax_AI",
    "OpenRouter",
    "steipete",
    "simile_ai",
    "berkeley_ai",
    "blackboxai",
    "UnslothAI",
    "openclaw",
    "Zread_ai",
]

X_API_BASE = "https://api.x.com/2"


def get_user_id(username: str, bearer_token: str) -> Optional[str]:
    """Get user ID from username."""
    url = f"{X_API_BASE}/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {"user.fields": "id,name,username"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]["id"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user ID for @{username}: {e}")
        return None


def get_user_tweets(user_id: str, start_time: str, bearer_token: str) -> list:
    """Get tweets for a user since start_time."""
    url = f"{X_API_BASE}/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    params = {
        "start_time": start_time,
        "max_results": 100,
        "tweet.fields": "id,text,created_at,public_metrics,edit_history_tweet_ids",
        "exclude": "retweets,replies",
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tweets for user {user_id}: {e}")
        return []


def calculate_engagement(tweet: dict) -> int:
    """Calculate total engagement for a tweet."""
    metrics = tweet.get("public_metrics", {})
    likes = metrics.get("like_count", 0)
    retweets = metrics.get("retweet_count", 0)
    replies = metrics.get("reply_count", 0)
    views = metrics.get("impression_count", 0)
    return likes + retweets + replies + views


def find_top_post(tweets: list) -> Optional[dict]:
    """Find the tweet with maximum engagement."""
    if not tweets:
        return None
    
    top_tweet = max(tweets, key=calculate_engagement)
    return top_tweet


def truncate_text(text: str, max_length: int = 120) -> str:
    """Truncate text to max_length and add ellipsis if needed."""
    # Remove newlines and extra whitespace
    text = " ".join(text.split())
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def create_tweet_link(tweet_id: str, username: str) -> str:
    """Create a link to the tweet."""
    return f"https://x.com/{username}/status/{tweet_id}"


def main():
    parser = argparse.ArgumentParser(description="Find top posts from X accounts")
    parser.add_argument("--days", type=int, default=1, help="Number of days to look back (default: 1)")
    parser.add_argument("--export", choices=["json"], help="Export results to JSON")
    args = parser.parse_args()

    bearer_token = os.environ.get("X_BEARER_TOKEN")
    if not bearer_token:
        print("Error: X_BEARER_TOKEN environment variable is not set")
        sys.exit(1)

    console = Console()
    
    # Calculate start time
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=args.days)
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    console.print(f"\n[bold blue]Searching for top posts from the last {args.days} day(s)...[/bold blue]\n")

    results = []

    for username in ACCOUNTS:
        # Get user ID
        user_id = get_user_id(username, bearer_token)
        if not user_id:
            console.print(f"[yellow]⚠ Could not find user @{username}[/yellow]")
            continue

        # Get tweets
        tweets = get_user_tweets(user_id, start_time_str, bearer_token)
        
        if not tweets:
            console.print(f"[dim]No tweets found for @{username}[/dim]")
            continue

        # Find top post
        top_tweet = find_top_post(tweets)
        if top_tweet:
            engagement = calculate_engagement(top_tweet)
            results.append({
                "username": username,
                "tweet_id": top_tweet["id"],
                "text": top_tweet["text"],
                "engagement": engagement,
                "likes": top_tweet.get("public_metrics", {}).get("like_count", 0),
                "retweets": top_tweet.get("public_metrics", {}).get("retweet_count", 0),
                "replies": top_tweet.get("public_metrics", {}).get("reply_count", 0),
                "views": top_tweet.get("public_metrics", {}).get("impression_count", 0),
                "created_at": top_tweet.get("created_at", ""),
                "link": create_tweet_link(top_tweet["id"], username),
            })

    # Sort by engagement descending
    results.sort(key=lambda x: x["engagement"], reverse=True)

    # Create table
    table = Table(title=f"Top Posts (Last {args.days} Day(s))", show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="cyan", justify="right", width=5)
    table.add_column("Account", style="green", width=18)
    table.add_column("Post Text", style="white", width=60)
    table.add_column("Engagement", style="yellow", justify="right", width=12)
    table.add_column("Link", style="blue", overflow="fold")

    for rank, result in enumerate(results, 1):
        truncated_text = truncate_text(result["text"], 58)
        table.add_row(
            str(rank),
            f"@{result['username']}",
            truncated_text,
            f"{result['engagement']:,}",
            result["link"],
        )

    if results:
        console.print(table)
    else:
        console.print("[red]No posts found with engagement data.[/red]")

    # Export to JSON if requested
    if args.export == "json":
        output_file = "top_posts.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        console.print(f"\n[green]✓ Results exported to {output_file}[/green]")

    # Print summary
    if results:
        console.print(f"\n[bold]Total accounts processed:[/bold] {len(ACCOUNTS)}")
        console.print(f"[bold]Accounts with posts:[/bold] {len(results)}")
        if results:
            console.print(f"[bold]Top post engagement:[/bold] {results[0]['engagement']:,} (@{results[0]['username']})")


if __name__ == "__main__":
    main()
