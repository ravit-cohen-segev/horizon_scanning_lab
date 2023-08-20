from abc import ABC, abstractmethod
from sagemaker.jumpstart.model import JumpStartModel
from sagemaker.huggingface import get_huggingface_llm_image_uri, HuggingFaceModel
import json
from tqdm import tqdm, trange
import time
import os



SAGE_ROLE = os.environ.get("SAGE_ROLE")

# In[]
class EndpointPredictor(ABC):
    def __init__(self, instance_type: str):
        self.instance_type = instance_type

    @abstractmethod
    def __create_model__(self):
        pass

    def generate_completions(self, prompts: list, parameters: dict):
        start_time = time.time()
        model = self.__create_model__()
        predictor = model.deploy(initial_instance_count=1, instance_type=self.instance_type,
                                 container_startup_health_check_timeout=300)
        print(f'Endpoint deployed in {round(time.time() - start_time, 1)} seconds')
        try:
            return [predict(predictor, prompt, parameters) for prompt in tqdm(prompts)]
        finally:
            predictor.delete_model()
            predictor.delete_endpoint()


class JumpStartPredictor(EndpointPredictor):

    # list of models available at https://sagemaker.readthedocs.io/en/stable/doc_utils/pretrainedmodels.html
    def __init__(self, model_id: str, instance_type: str):
        super().__init__(instance_type)
        self.model_id = model_id

    def __create_model__(self):
        print(f"Using {self.model_id}")
        return JumpStartModel(model_id=self.model_id, role=SAGE_ROLE)


class HuggingFacePredictor(EndpointPredictor):

    # list of models available at hf.co/models
    def __init__(self, model_id: str, instance_type: str, num_gpu: int, max_input_tokens: int = 1536,
                 max_output_tokens: int = 512, quantize: bool = False):
        super().__init__(instance_type)
        config = {
            'HF_MODEL_ID': model_id,
            'SM_NUM_GPUS': json.dumps(num_gpu),
            'MAX_INPUT_LENGTH': json.dumps(max_input_tokens),
            'MAX_TOTAL_TOKENS': json.dumps(max_input_tokens + max_output_tokens),
        }
        if quantize:
            config['HF_MODEL_QUANTIZE'] = "bitsandbytes"
        self.model_id = model_id
        self.config = config

    def __create_model__(self):
        print(f"Using {self.model_id}")
        llm_image = get_huggingface_llm_image_uri("huggingface", version="0.8.2")
        return HuggingFaceModel(role=SAGE_ROLE, image_uri=llm_image, env=self.config)


def predict(predictor, prompt, parameters):
    payload = {
        'inputs': prompt,
        'parameters': parameters
    }
    return predictor.predict(payload, custom_attributes="accept_eula=true")
