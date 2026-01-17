def lambda_handler(event, context):
    print("Validating data...")
    print(f"Input event: {event}")

    return {
        "status": "validated",
        "input": event
    }
