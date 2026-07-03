import unittest
from pathlib import Path

from app.services.ml_training.inference_artifact_savers import (
    build_report_name,
    ensure_report_dir,
    save_inference_report,
    save_report_text,
)
from app.services.ml_training.run_ml_inference_pipeline import (
    MlInferencePipelineResult,
)


def build_pipeline_result() -> MlInferencePipelineResult:
    """Build ML inference pipeline result for artifact saver tests.
    Args:
        """
    prediction_rows = [
        {
            'source_row_index': 0,
            'predicted_value': 1.5,
            'client_id': 1,
            'company_id': 10,
            'vacancy_id': 100,
            'date_day': '2025-09-01',
        },
        {
            'source_row_index': 1,
            'predicted_value': 2.5,
            'client_id': 1,
            'company_id': 11,
            'vacancy_id': 101,
            'date_day': '2025-09-02',
        },
    ]

    return MlInferencePipelineResult(
        ml_training_run_id=1,
        training_run_name='ml_training_2026-06-21_21-23-44',
        ml_dataset_run_id=10,
        client_id=1,
        model_path='artifacts/models/pipeline_3/model.cbm',
        row_count=2,
        prediction_row_count=2,
        predictions=[1.5, 2.5],
        prediction_rows=prediction_rows,
    )


class TestInferenceArtifactSavers(unittest.TestCase):
    """Test ML inference artifact savers."""

    def test_build_report_name(self) -> None:
        """Test ML inference report name building.
        Args:
            """
        result = build_report_name(
            training_run_name='ml_training_2026-06-21_21-23-44',
        )

        self.assertEqual(
            result,
            'ml_inference_2026-06-21_21-23-44.md',
        )

    def test_build_custom_name(self) -> None:
        """Test custom ML inference report name building.
        Args:
            """
        result = build_report_name(
            training_run_name='custom_training_run',
        )

        self.assertEqual(
            result,
            'ml_inference_custom_training_run.md',
        )

    def test_ensure_report_dir(self) -> None:
        """Test ML inference report directory creation.
        Args:
            """
        temp_dir = Path('tmp_test_inference_reports')

        try:
            result = ensure_report_dir(reports_dir=temp_dir)

            self.assertTrue(result.exists())
            self.assertTrue(result.is_dir())
        finally:
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_save_report_text(self) -> None:
        """Test ML inference report text saving.
        Args:
            """
        temp_dir = Path('tmp_test_inference_reports')
        report_name = 'ml_inference_test.md'

        try:
            report_path = save_report_text(
                report_text='# Test Report',
                report_name=report_name,
                reports_dir=temp_dir,
            )
            saved_path = Path(report_path)

            self.assertTrue(saved_path.exists())
            self.assertEqual(
                saved_path.read_text(encoding='utf-8'),
                '# Test Report',
            )
        finally:
            saved_path = temp_dir / report_name

            if saved_path.exists():
                saved_path.unlink()

            if temp_dir.exists():
                temp_dir.rmdir()

    def test_save_inference_report(self) -> None:
        """Test ML inference report artifact saving.
        Args:
            """
        temp_dir = Path('tmp_test_inference_reports')
        result = build_pipeline_result()

        try:
            report_path = save_inference_report(
                result=result,
                reports_dir=temp_dir,
            )
            saved_path = Path(report_path)
            report_text = saved_path.read_text(encoding='utf-8')

            self.assertTrue(saved_path.exists())
            self.assertEqual(
                saved_path.name,
                'ml_inference_2026-06-21_21-23-44.md',
            )
            self.assertIn('# ML Inference Report', report_text)
            self.assertIn('## Run Metadata', report_text)
            self.assertIn('## Prediction Summary', report_text)
            self.assertIn('| Mean Prediction | 2.000000 |', report_text)
        finally:
            saved_path = temp_dir / 'ml_inference_2026-06-21_21-23-44.md'

            if saved_path.exists():
                saved_path.unlink()

            if temp_dir.exists():
                temp_dir.rmdir()
