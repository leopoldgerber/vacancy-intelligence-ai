import unittest

from app.services.ml_training.inference_report_builders import (
    InferencePredictionSummary,
    build_inference_report,
    build_metadata_table,
    build_prediction_table,
    build_summary_table,
    format_value,
    summarize_predictions,
)
from app.services.ml_training.run_ml_inference_pipeline import (
    MlInferencePipelineResult,
)


def build_pipeline_result() -> MlInferencePipelineResult:
    """Build ML inference pipeline result for report tests.
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


class TestInferenceReportBuilders(unittest.TestCase):
    """Test ML inference report builders."""

    def test_format_value(self) -> None:
        """Test report value formatting.
        Args:
            """
        self.assertEqual(format_value(value=None), '')
        self.assertEqual(format_value(value=1.2345678), '1.234568')
        self.assertEqual(format_value(value='value'), 'value')

    def test_summarize_predictions(self) -> None:
        """Test inference prediction summary.
        Args:
            """
        result = summarize_predictions(predictions=[1.5, 2.5, 3.5])

        self.assertEqual(
            result,
            InferencePredictionSummary(
                prediction_count=3,
                mean_prediction=2.5,
                min_prediction=1.5,
                max_prediction=3.5,
            ),
        )

    def test_summarize_empty(self) -> None:
        """Test empty inference prediction summary.
        Args:
            """
        result = summarize_predictions(predictions=[])

        self.assertEqual(
            result,
            InferencePredictionSummary(
                prediction_count=0,
                mean_prediction=None,
                min_prediction=None,
                max_prediction=None,
            ),
        )

    def test_build_metadata_table(self) -> None:
        """Test inference metadata table building.
        Args:
            """
        result = build_pipeline_result()

        report_table = build_metadata_table(result=result)

        self.assertIn('| ML Training Run ID | 1 |', report_table)
        self.assertIn(
            '| Training Run Name | ml_training_2026-06-21_21-23-44 |',
            report_table,
        )
        self.assertIn('| Prediction Rows | 2 |', report_table)

    def test_build_summary_table(self) -> None:
        """Test inference summary table building.
        Args:
            """
        summary = summarize_predictions(predictions=[1.5, 2.5])

        report_table = build_summary_table(summary=summary)

        self.assertIn('| Prediction Count | 2 |', report_table)
        self.assertIn('| Mean Prediction | 2.000000 |', report_table)
        self.assertIn('| Min Prediction | 1.500000 |', report_table)
        self.assertIn('| Max Prediction | 2.500000 |', report_table)

    def test_build_prediction_table(self) -> None:
        """Test inference prediction table building.
        Args:
            """
        result = build_pipeline_result()

        report_table = build_prediction_table(
            prediction_rows=result.prediction_rows,
        )

        self.assertIn(
            (
                '| Source Row | Client ID | Company ID | '
                'Vacancy ID | Date | Prediction |'
            ),
            report_table,
        )
        self.assertIn(
            '| 0 | 1 | 10 | 100 | 2025-09-01 | 1.500000 |',
            report_table,
        )

    def test_build_empty_table(self) -> None:
        """Test empty inference prediction table building.
        Args:
            """
        report_table = build_prediction_table(prediction_rows=[])

        self.assertEqual(report_table, 'No prediction rows.')

    def test_build_inference_report(self) -> None:
        """Test inference markdown report building.
        Args:
            """
        result = build_pipeline_result()

        report = build_inference_report(result=result)

        self.assertIn('# ML Inference Report', report)
        self.assertIn('## Run Metadata', report)
        self.assertIn('## Prediction Summary', report)
        self.assertIn('## Sample Predictions', report)
        self.assertIn('| Mean Prediction | 2.000000 |', report)
