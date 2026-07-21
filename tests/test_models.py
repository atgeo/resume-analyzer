# tests/test_models.py

from models import ResumeSummary, Job


def test_is_currently_working_true():
    summary = ResumeSummary(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        jobs=[
            Job(
                company="Acme",
                title="Developer",
                start_date="2024-01",
                end_date=None,
                is_current=True,
            )
        ],
        education=[],
    )

    assert summary.is_currently_working is True


def test_is_currently_working_false():
    summary = ResumeSummary(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        jobs=[
            Job(
                company="Acme",
                title="Developer",
                start_date="2022",
                end_date="2024",
                is_current=False,
            )
        ],
        education=[],
    )

    assert summary.is_currently_working is False
