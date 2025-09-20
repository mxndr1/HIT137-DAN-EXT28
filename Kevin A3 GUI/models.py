from transformers import pipeline


# Encapsulation: AIModel hides internal pipeline logic
class AIModel:
    def __init__(self, name, task, model_id):
        self.name = name
        self.task = task
        self.model_id = model_id
        self.pipeline = pipeline(task, model=model_id)

    def run(self, input_data):
        return self.pipeline(input_data)


# Polymorphism: subclasses override the run method
class TextClassificationModel(AIModel):
    def run(self, input_data):
        result = super().run(input_data)
        return result[0]  # return first classification result


class TextGenerationModel(AIModel):
    def run(self, input_data):
        result = super().run(input_data)
        return result[0]["generated_text"]


# Composition: manage multiple models
class ModelManager:
    def __init__(self):
        self.models = {
            "Sentiment Analysis": TextClassificationModel(
                "Sentiment Analysis",
                "text-classification",
                "distilbert-base-uncased-finetuned-sst-2-english"
            ),
            "Text Generation": TextGenerationModel(
                "Text Generation",
                "text-generation",
                "distilgpt2"
            )
        }

    def run(self, model_name, input_data):
        model = self.models.get(model_name)
        if model:
            return model.run(input_data)
        return "Model not found"