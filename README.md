# Kafka to Hudi with Delta Streamer

Produce Data to Kafka

```sh
python scripts/kproducer.py
```

Run DeltaStreamer job to create Hudi table

```sh
export SPARK_LOCAL_HOSTNAME=localhost

spark-submit --packages org.apache.spark:spark-avro_2.12:3.0.0 \
  --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer `ls ~/dev/packages/hudi-utilities-bundle_2.12-0.9.0.jar` \
  --props file://${PWD}/configs/kafka-source.properties \
  --source-class org.apache.hudi.utilities.sources.JsonKafkaSource \
  --schemaprovider-class org.apache.hudi.utilities.schema.FilebasedSchemaProvider \
  --payload-class org.apache.hudi.common.model.OverwriteNonDefaultsWithLatestAvroPayload \
  --target-base-path /tmp/hudi/test_table \
  --target-table test_table \
  --table-type COPY_ON_WRITE \
  --op BULK_INSERT \
  --transformer-class org.apache.hudi.utilities.transform.SqlQueryBasedTransformer \
  --hoodie-conf hoodie.deltastreamer.transformer.sql="SELECT a.event.name, a.event.number, a.event.date FROM <SRC> a"

```

Query the Hudi table

```sh
spark-shell \
  --packages org.apache.hudi:hudi-spark3.3-bundle_2.12:0.12.0 \
  --conf 'spark.serializer=org.apache.spark.serializer.KryoSerializer' \
  --conf 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog' \
  --conf 'spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension'
```

```scala
val basePath = "file:///tmp/hudi/test_table"
val testSnapshotDF = spark.
  read.
  format("hudi").
  load(basePath)
testSnapshotDF.createOrReplaceTempView("test_table")

spark.sql("select * from  test_table limit 10").show()
```
