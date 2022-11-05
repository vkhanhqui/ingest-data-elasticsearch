from pyspark.sql import SparkSession


if __name__ == '__main__':
    spark = SparkSession.builder\
        .appName('Ingest data to OpenSearch')\
        .config(
            'spark.jars',
            'es-jars/elasticsearch-spark-30_2.12-8.5.0.jar'
        ).getOrCreate()
    print('-----end----init------')
    df = spark.read\
        .options(
            inferSchema=True,
            header=True
        ).json(
            'zalo/wikipedia_20220620_cleaned/wikipedia_20220620_cleaned.json'
        )
    print('-----end---read------')
    df.write \
        .mode('overwrite') \
        .format('org.elasticsearch.spark.sql') \
        .option('es.nodes', 'localhost') \
        .option('es.port', 9200) \
        .option('es.net.ssl', 'false') \
        .option('es.net.http.auth.user', 'elastic') \
        .option('es.net.http.auth.pass', 'Cd2IDe=0Kq51WFIAZDH2') \
        .option('es.nodes.wan.only', 'true') \
        .option('es.nodes.discovery', 'false') \
        .option('es.resource', 'wiki-cleaned') \
        .option('es.index.auto.create', 'true') \
        .option('es.mapping.id', 'id') \
        .option('es.write.operation', 'index') \
        .option('es.batch.size.entries', '100') \
        .option('es.batch.write.retry.policy', 'simple') \
        .option('es.batch.write.retry.count', '-1') \
        .option('es.batch.write.retry.limit', '-1') \
        .option('es.batch.write.retry.wait', '30s') \
        .save()
