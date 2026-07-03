from pathlib import Path
from typing import TYPE_CHECKING

from app.services.ml_training.inference_report_builders import (
    build_inference_report,
)


if TYPE_CHECKING:
    from app.services.ml_training.run_ml_inference_pipeline import (
        MlInferencePipelineResult,
    )


INFERENCE_REPORTS_DIR = Path('artifacts/reports/pipeline_3/inference')
MARKDOWN_EXTENSION = '.md'


def build_report_name(training_run_name: str) -> str:
    """Build ML inference report file name.
    Args:
        training_run_name (str): Source ML training run name."""
    if training_run_name.startswith('ml_training_'):
        report_base_name = training_run_name.replace(
            'ml_training_',
            'ml_inference_',
            1,
        )
    else:
        report_base_name = f'ml_inference_{training_run_name}'

    return f'{report_base_name}{MARKDOWN_EXTENSION}'


def ensure_report_dir(reports_dir: str | Path) -> Path:
    """Ensure ML inference report directory exists.
    Args:
        reports_dir (str | Path): Report directory path."""
    resolved_dir = Path(reports_dir)
    resolved_dir.mkdir(parents=True, exist_ok=True)

    return resolved_dir


def save_report_text(
    report_text: str,
    report_name: str,
    reports_dir: str | Path = INFERENCE_REPORTS_DIR,
) -> str:
    """Save ML inference report text.
    Args:
        report_text (str): Markdown report text.
        report_name (str): Markdown report file name.
        reports_dir (str | Path): Report directory path."""
    resolved_dir = ensure_report_dir(reports_dir=reports_dir)
    report_path = resolved_dir / report_name
    report_path.write_text(report_text, encoding='utf-8')

    return str(report_path)


def save_inference_report(
    result: 'MlInferencePipelineResult',
    reports_dir: str | Path = INFERENCE_REPORTS_DIR,
) -> str:
    """Save ML inference markdown report.
    Args:
        result (MlInferencePipelineResult): ML inference pipeline result.
        reports_dir (str | Path): Report directory path."""
    report_name = build_report_name(
        training_run_name=result.training_run_name,
    )
    report_text = build_inference_report(result=result)

    return save_report_text(
        report_text=report_text,
        report_name=report_name,
        reports_dir=reports_dir,
    )
