import asyncio
import math
import time

from app.services.analysis_pipeline import AnalysisPipeline


def generate_large_text(target_bytes: int = 2_000_000) -> str:
    """Generate a synthetic large text block around the target size."""
    sample_paragraph = (
        "Artificial intelligence enables machines to learn from data, "
        "identify patterns, and make decisions with minimal human intervention. "
        "In modern applications, large language models analyze diverse corpora "
        "to understand context, semantics, and stylistic nuances. "
        "Researchers often benchmark models on extensive datasets to gauge "
        "robustness and performance across tasks. "
    )
    repetitions = math.ceil(target_bytes / len(sample_paragraph))
    return " \n".join(sample_paragraph for _ in range(repetitions))


def summarize_pipeline_result(result):
    """Extract the most relevant performance metrics from the pipeline result."""
    metrics = {
        "status": result.status.value,
        "text_bytes": result.metadata.file_size_bytes if result.metadata else None,
        "processing_time_seconds": result.metadata.processing_time_seconds if result.metadata else None,
        "keyness_time_ms": result.keyness.processing_time_ms if result.keyness else None,
        "clustering_time_ms": result.semanticClustering.processing_time_ms if result.semanticClustering else None,
        "sentiment_time_ms": result.sentiment.processing_time_ms if result.sentiment else None,
        "total_keywords": result.keyness.total_keywords if result.keyness else None,
        "total_clusters": result.semanticClustering.total_clusters if result.semanticClustering else None,
        "model_versions": result.metadata.model_versions if result.metadata else {},
    }
    return metrics


async def run_performance_test():
    pipeline = AnalysisPipeline()
    large_text = generate_large_text()

    print("Generated dataset size:", len(large_text.encode("utf-8")), "bytes")

    start = time.perf_counter()
    result = await pipeline.analyze(large_text, analysis_id="perf-large-dataset")
    end = time.perf_counter()

    metrics = summarize_pipeline_result(result)
    metrics["wall_clock_seconds"] = end - start

    print("Performance metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(run_performance_test())