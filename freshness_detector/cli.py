"""
Freshness Detector - Command Line Interface
"""
import argparse
import json
import sys
from datetime import datetime
from typing import Optional

from .core import (
    calculate_freshness,
    check_dataset,
    batch_check,
    DecayPolicy,
    age_in_days
)


def cmd_calculate(args):
    """Calculate freshness for a single data point"""
    try:
        freshness = calculate_freshness(
            args.confidence,
            args.timestamp,
            args.topic,
            custom_lambda=args.lambda_val if hasattr(args, 'lambda_val') else None,
            custom_floor=args.floor if hasattr(args, 'floor') else None
        )
        
        policy = DecayPolicy.get_policy(args.topic)
        age = age_in_days(args.timestamp)
        
        print("🧪 Freshness Analysis")
        print("=" * 50)
        print(f"Initial confidence: {args.confidence:.1%}")
        print(f"Capture timestamp:  {args.timestamp}")
        print(f"Age:                {age:.1f} days")
        print(f"Topic type:         {args.topic}")
        print(f"Decay policy:       {policy.name}")
        print(f"Decay rate (λ):     {policy.lambda_per_day:.4f} per day")
        print(f"Floor:              {policy.floor:.1%}")
        print("=" * 50)
        print(f"Current confidence: {freshness:.1%}")
        
        if freshness < 0.3:
            print("⚠️  WARNING: Data is STALE (< 30% confidence)")
        elif freshness < 0.5:
            print("⚠️  CAUTION: Data is aging (< 50% confidence)")
        elif freshness < 0.7:
            print("✓  OK: Data is acceptable (50-70% confidence)")
        else:
            print("✓  FRESH: Data is fresh (> 70% confidence)")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_check(args):
    """Check a dataset file for stale entries"""
    try:
        results = check_dataset(
            args.dataset,
            topic_type=args.topic,
            threshold=args.threshold
        )
        
        if "error" in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            return 1
        
        # Print summary
        print(results["summary"])
        
        # Print alerts if requested
        if args.verbose and results["alerts"]:
            print("\n" + "=" * 50)
            print("STALE ENTRIES:")
            print("=" * 50)
            for alert in results["alerts"][:args.max_alerts]:
                print(f"\nEntry #{alert['index']}:")
                print(f"  Timestamp:  {alert['timestamp']}")
                print(f"  Age:        {alert['age_days']:.1f} days")
                print(f"  Confidence: {alert['confidence']:.1%}")
                print(f"  Reason:     {alert['reason']}")
            
            if len(results["alerts"]) > args.max_alerts:
                remaining = len(results["alerts"]) - args.max_alerts
                print(f"\n... and {remaining} more stale entries")
        
        # Export results if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results exported to {args.output}")
        
        # Exit with error code if stale entries found
        return 1 if results["stale_entries"] > 0 else 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_policies(args):
    """List all available decay policies"""
    print("📋 Available Decay Policies")
    print("=" * 70)
    
    for policy_name in DecayPolicy.list_policies():
        policy = DecayPolicy.get_policy(policy_name)
        print(f"\n{policy_name.upper()}")
        print(f"  Name:        {policy.name}")
        print(f"  Decay rate:  {policy.lambda_per_day:.4f} per day")
        print(f"  Floor:       {policy.floor:.1%}")
        print(f"  Description: {policy.description}")
    
    print("\n" + "=" * 70)
    print("Usage: freshness calculate --topic <policy_name> ...")
    
    return 0


def cmd_demo(args):
    """Run a quick demo"""
    print("🧪 Freshness Detector Demo")
    print("=" * 70)
    
    examples = [
        ("2025-12-01", 0.95, "ai_training", "Recent AI training data"),
        ("2024-06-01", 0.90, "ai_training", "6-month-old AI training data"),
        ("2023-01-01", 0.85, "ai_training", "2-year-old AI training data"),
        ("2025-12-01", 0.90, "news", "Recent news"),
        ("2024-01-01", 0.90, "news", "1-year-old news"),
        ("2020-01-01", 0.95, "history", "Historical fact"),
    ]
    
    for timestamp, confidence, topic, description in examples:
        freshness = calculate_freshness(confidence, timestamp, topic)
        age = age_in_days(timestamp)
        
        print(f"\n{description}:")
        print(f"  Timestamp:  {timestamp}")
        print(f"  Age:        {age:.0f} days")
        print(f"  Topic:      {topic}")
        print(f"  Initial:    {confidence:.1%}")
        print(f"  Current:    {freshness:.1%}")
        
        if freshness < 0.3:
            status = "⚠️  STALE"
        elif freshness < 0.5:
            status = "⚠️  AGING"
        elif freshness < 0.7:
            status = "✓  OK"
        else:
            status = "✓  FRESH"
        print(f"  Status:     {status}")
    
    print("\n" + "=" * 70)
    print("Try: freshness check <your_dataset.json>")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="freshness",
        description="Freshness Detector - Detect stale AI training data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate freshness of a single data point
  freshness calculate --confidence 0.9 --timestamp "2025-01-01" --topic science
  
  # Check a dataset for stale entries
  freshness check training_data.json --threshold 0.4
  
  # List all decay policies
  freshness policies
  
  # Run demo
  freshness demo

For more information: https://github.com/infrastructure-observatory/freshness-detector
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Calculate command
    calc_parser = subparsers.add_parser(
        "calculate",
        help="Calculate freshness score for a single data point"
    )
    calc_parser.add_argument(
        "--confidence", "-c",
        type=float,
        default=1.0,
        help="Initial confidence (0.0-1.0, default: 1.0)"
    )
    calc_parser.add_argument(
        "--timestamp", "-t",
        required=True,
        help="Capture timestamp (ISO format, e.g., 2025-01-01)"
    )
    calc_parser.add_argument(
        "--topic", "-p",
        default="ai_training",
        help="Topic type (news, science, code, medical, ai_training, etc.)"
    )
    calc_parser.set_defaults(func=cmd_calculate)
    
    # Check command
    check_parser = subparsers.add_parser(
        "check",
        help="Check a dataset file for stale entries"
    )
    check_parser.add_argument(
        "dataset",
        help="Path to dataset file (JSON or JSONL)"
    )
    check_parser.add_argument(
        "--threshold", "-T",
        type=float,
        default=0.3,
        help="Confidence threshold (0.0-1.0, default: 0.3)"
    )
    check_parser.add_argument(
        "--topic", "-p",
        default="ai_training",
        help="Topic type"
    )
    check_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed alerts for stale entries"
    )
    check_parser.add_argument(
        "--max-alerts",
        type=int,
        default=10,
        help="Maximum number of alerts to display (default: 10)"
    )
    check_parser.add_argument(
        "--output", "-o",
        help="Export results to JSON file"
    )
    check_parser.set_defaults(func=cmd_check)
    
    # Policies command
    policies_parser = subparsers.add_parser(
        "policies",
        help="List all available decay policies"
    )
    policies_parser.set_defaults(func=cmd_policies)
    
    # Demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run a quick demonstration"
    )
    demo_parser.set_defaults(func=cmd_demo)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
