import httpx
import asyncio
import itertools


class PredictionFetcher():

    def __init__(self, generator_host, generator_port, models):
        self.generator_api_url = f"http://{generator_host}:{generator_port}/generate"
        self.models = models
        self.event_loop = asyncio.new_event_loop()

    def fetch_predictions(self, viewer_id):
        result = self.event_loop.run_until_complete(self.__fetch_all_predictions__(viewer_id, self.models))
        return result

    async def __fetch_all_predictions__(self, viewer_id, models):
        async with httpx.AsyncClient() as client:
            return await asyncio.gather(
                *map(self.__request_prediction__, models, itertools.repeat(viewer_id), itertools.repeat(client),)
            )

    async def __request_prediction__(self, model_name, viewer_id, httpx_client):
        response = await httpx_client.post(self.generator_api_url, params={'model_name': model_name, 'viewerid': viewer_id})
        return response.json()
