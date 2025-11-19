"""Main entry point for Nuclear Industry Intelligence System.

This module provides a command-line interface for executing intelligence
gathering workflows with configurable topics and parameters.
"""

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from nuclear_intelligence.crew import NuclearIntelligenceCrew

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Nuclear Industry Intelligence System."""
    parser = argparse.ArgumentParser(
        description="Nuclear Industry Intelligence System - Multi-agent AI system "
        "for radiation safety information aggregation and synthesis"
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Topic or area of focus for intelligence gathering "
        "(e.g., 'ALARA implementation', 'dosimetry advances', 'regulatory updates')",
    )
    parser.add_argument(
        "--time-window",
        type=str,
        default="past month",
        help="Time window for information discovery (default: 'past month')",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory for output files (default: outputs/ in project root)",
    )

    args = parser.parse_args()

    try:
        # Initialize crew
        crew = NuclearIntelligenceCrew(output_dir=args.output_dir)

        # Execute workflow
        result = crew.kickoff(
            topic=args.topic,
            time_window=args.time_window,
        )

        logger.info("Workflow completed successfully")
        logger.info(f"Output directory: {crew.output_dir}")

        return 0

    except KeyboardInterrupt:
        logger.info("Workflow interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error during workflow execution: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())


