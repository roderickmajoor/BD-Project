from pyspark.sql import DataFrame
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType
import logging


class ConvertToBoolean:
    def __init__(self, input_column_name: str, output_column_name: str, mapping: dict):
        """
        Initializes the module to convert column values to boolean based on a provided mapping.

        Parameters:
        - input_column_name: The name of the input column to apply the conversion on.
        - output_column_name: The name of the output column for the conversion results.
        - mapping: A dictionary mapping of original values to boolean values.
        """
        self.input_column_name = input_column_name
        self.output_column_name = output_column_name
        self.mapping = mapping

    def process(self, df: DataFrame) -> DataFrame:
        """
        Converts column values to boolean in the PySpark DataFrame based on the specified mapping.

        Parameters:
        - df: The PySpark DataFrame to apply the conversion on.

        Returns:
        - The PySpark DataFrame with the specified column's values converted to boolean.
        """
        # Define a UDF to convert values based on the provided mapping and log a warning if the value is not in the mapping
        def convert_value(value):
            if value in self.mapping:
                return self.mapping[value]
            else:
                # logging.warning(f"Encountered an unexpected value '{value}' in column '{self.input_column_name}' that is not defined in the mapping. Returning None.")
                return None

        convert_to_boolean_udf = udf(convert_value, BooleanType())

        # Apply the conversion to the specified column
        original_count = df.count()
        df = df.withColumn(self.output_column_name, convert_to_boolean_udf(col(self.input_column_name)))
        # drop None values
        df = df.filter(col(self.output_column_name).isNotNull())
        new_count = df.count()
        diff = original_count - new_count
        if diff > 0:
            logging.warning(f"⚠️ Dropped {diff}/{original_count} rows.")
        return df