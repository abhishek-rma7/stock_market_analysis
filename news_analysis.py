import random
from google.cloud import language_v1

tech_giants = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Google': 'GOOGL',
    'Facebook': 'FB',
    'Tesla': 'TSLA',
    'Nvidia': 'NVDA',
    'Intel': 'INTC',
    'Adobe': 'ADBE',
    'Netflix': 'NFLX'
}

sentiment_intervals = {
    (-1.0, -0.97): (-3.12, -3.21),
    (-0.97, -0.94): (-3.01, -3.11),
    (-0.94, -0.91): (-2.91, -3.01),
    (-0.91, -0.88): (-2.81, -2.91),
    (-0.88, -0.85): (-2.71, -2.81),
    (-0.85, -0.82): (-2.61, -2.71),
    (-0.82, -0.79): (-2.51, -2.61),
    (-0.79, -0.76): (-2.41, -2.51),
    (-0.76, -0.73): (-2.21, -2.31),
    (-0.73, -0.70): (-2.16, -2.20),
    (-0.70, -0.67): (-2.10, -2.15),
    (-0.67, -0.64): (-2.01, -2.08),
    (-0.64, -0.61): (-1.91, -2.00),
    (-0.61, -0.58): (-1.80, -1.90),
    (-0.58, -0.55): (-1.69, -1.78),
    (-0.55, -0.52): (-1.62, -1.68),
    (-0.52, -0.49): (-1.56, -1.61),
    (-0.49, -0.46): (-1.48, -1.55),
    (-0.46, -0.43): (-1.43, -1.47),
    (-0.43, -0.40): (-1.37, -1.42),
    (-0.40, -0.37): (-1.33, -1.36),
    (-0.37, -0.34): (-1.26, -1.32),
    (-0.34, -0.31): (-1.19, -1.25),
    (-0.31, -0.28): (-1.12, -1.18),
    (-0.28, -0.25): (-1.08, -1.11),
    (-0.25, -0.22): (-1.05, -1.07),
    (-0.22, -0.19): (-1.00, -1.04),
    (-0.19, -0.16): (-0.22, -0.19),
    (-0.16, -0.13): (-0.19, -0.16),
    (-0.13, -0.10): (-0.16, -0.13),
    (-0.10, -0.07): (-0.13, -0.10),
    (-0.07, -0.04): (-0.10, -0.07),
    (-0.04, -0.01): (-0.07, -0.04),
    (-0.01, 0.02): (-0.04, -0.01),
    (0.02, 0.05): (0.01, 0.04),
    (0.05, 0.08): (0.04, 0.07),
    (0.08, 0.11): (0.07, 0.10),
    (0.11, 0.14): (0.10, 0.13),
    (0.14, 0.17): (0.14, 0.17),
    (0.17, 0.20): (0.16, 0.19),
    (0.20, 0.23): (0.19, 0.22),
    (0.23, 0.26): (0.22, 0.25),
    (0.26, 0.29): (0.25, 0.28),
    (0.29, 0.32): (0.28, 0.31),
    (0.32, 0.35): (0.40, 0.43),
    (0.35, 0.38): (0.46, 0.49),
    (0.38, 0.41): (0.49, 0.51),
    (0.41, 0.44): (0.52, 0.54),
    (0.44, 0.47): (0.55, 0.58),
    (0.47, 0.50): (0.61, 0.64),
    (0.50, 0.53): (0.65, 0.68),
    (0.53, 0.56): (0.69, 0.72),
    (0.56, 0.59): (0.72, 0.75),
    (0.59, 0.62): (0.76, 0.79),
    (0.62, 0.65): (0.81, 0.84),
    (0.65, 0.68): (0.85, 0.88),
    (0.68, 0.71): (0.89, 0.92),
    (0.71, 0.74): (0.93, 0.95),
    (0.74, 0.77): (0.96, 0.99),
    (0.77, 0.80): (1.02, 1.05),
    (0.80, 0.83): (1.06, 1.12),
    (0.83, 0.86): (1.13, 1.17),
    (0.86, 0.89): (1.18,1.22),
    (0.89, 0.92): (1.23, 1.27),
    (0.92, 0.95): (1.28, 1.32),
    (0.95, 0.98): (1.35, 1.38),
    (0.98, 1.0): (1.40, 2)
}


def sample_analyze_entity_sentiment(text_content):

    print(f"Headline: {text_content}")
    client = language_v1.LanguageServiceClient(
        client_options={"credentials_file": "credentials.json"}
    )

    type_ = language_v1.types.Document.Type.PLAIN_TEXT

    data_to_send = {}
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    data_to_send["sentences"] = {
        "score": response.document_sentiment.score,
        "magnitude": response.document_sentiment.magnitude
    };

    document_sentiment = response.document_sentiment.score

    response = client.analyze_entity_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    for entity in response.entities:
        entity_type = "{}".format(language_v1.Entity.Type(entity.type_).name)

        if entity_type == "ORGANIZATION":
            org_name = entity.name
            for company, ticker in tech_giants.items():
                if company.lower() in text_content.lower():
                    sentiment = entity.sentiment

                    for interval, change_range in sentiment_intervals.items():
                        if interval[0] <= sentiment.score + document_sentiment < interval[1]:
                            stock_change = random.uniform(change_range[0], change_range[1])
                            print("{} sentiment score: {}".format(org_name, sentiment.score))
                            print("{} sentiment magnitude: {}".format(org_name, sentiment.magnitude))
                            print(f"Percentage Change: {stock_change:.2f}%")

                            data_to_send[ticker] = {
                                "sentiment": sentiment.score,
                                "change": f'{stock_change:.2f}'
                            }
                            break
        print("==============")

    return data_to_send


sample_analyze_entity_sentiment("Google to destroy browsing data to settle consumer privacy lawsuit")
