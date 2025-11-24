import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, round as spark_round, when, lit
from datetime import datetime

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

print("Starting COVID data transformation job...")

input_path = "s3://healthcare-datalake-anagha/raw/covid/"
output_path = "s3://healthcare-datalake-anagha/processed/covid/"

print(f"Reading data from: {input_path}")
df = spark.read.option("header", "true").option("inferSchema", "true").csv(input_path)

print(f"Records read: {df.count()}")

df_clean = df.filter(col("country").isNotNull())

df_transformed = df_clean.withColumn(
    "death_rate_pct",
    when(col("cases") > 0, 
         spark_round((col("deaths") / col("cases")) * 100, 2)
    ).otherwise(0)
)

df_transformed = df_transformed.withColumn(
    "recovery_rate_pct",
    when(col("cases") > 0,
         spark_round((col("recovered") / col("cases")) * 100, 2)
    ).otherwise(0)
)

df_transformed = df_transformed.withColumn(
    "active_rate_pct",
    when(col("cases") > 0,
         spark_round((col("active") / col("cases")) * 100, 2)
    ).otherwise(0)
)

df_transformed = df_transformed.withColumn(
    "severity_level",
    when(col("activePerOneMillion") > 5000, "High")
    .when(col("activePerOneMillion") > 1000, "Medium")
    .when(col("activePerOneMillion") > 0, "Low")
    .otherwise("Minimal")
)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
df_transformed = df_transformed.withColumn("processed_at", lit(current_time))

df_final = df_transformed.select(
    "country",
    "continent",
    "population",
    "cases",
    "todayCases",
    "deaths",
    "todayDeaths",
    "recovered",
    "active",
    "critical",
    "death_rate_pct",
    "recovery_rate_pct",
    "active_rate_pct",
    "severity_level",
    "casesPerOneMillion",
    "deathsPerOneMillion",
    "testsPerOneMillion",
    "processed_at"
)

print(f"Transformed records: {df_final.count()}")
print(f"Writing to: {output_path}")

df_final.write.mode("overwrite").parquet(output_path)

print("✅ Transformation complete!")

job.commit()
