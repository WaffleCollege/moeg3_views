# OpenAIのAPIサーバと通信

# openAIをインポート
import os
from openai import OpenAI
# OpenAI API KEY(環境変数推奨→.envで環境変数を設定済)
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
