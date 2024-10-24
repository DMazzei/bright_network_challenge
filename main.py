import click

from job_recommendation.http_client import Client
from job_recommendation.matching_algorithm import MatchingAlgorithm


@click.command()
@click.option(
    "--all",
    "-a",
    is_flag=True,
    help="Present all jobs for candidate, ordered by recommendation score.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show extra information, including the candidate`s bio.",
)
@click.option("--list-jobs", "-l", is_flag=True, help="List available jobs.")
def main(all, verbose, list_jobs):
    jobs = Client().get_jobs()
    candidates = Client().get_candidates()

    if list_jobs:
        print("List of available jobs:\n")
        for job in jobs:
            print(f"> {job.title} in {job.location}")
    print("\n------------------------------\n")
    matching_tool = MatchingAlgorithm(jobs)

    for candidate in candidates:
        print(f"Recommendations for {candidate.name}:")
        if verbose:
            print(f" Bio: {candidate.bio}\n")
        for job in matching_tool.get_recommendations(candidate=candidate, all_jobs=all):
            print(f" - {job.title} in {job.location}")
        print("------------------------------\n")


if __name__ == "__main__":
    main()
