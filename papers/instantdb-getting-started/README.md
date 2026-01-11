execution start time: 1/3/2026, 9:19:44 PM 
时间: 2026-01-03 13:19:44
时间: 2026-01-04 03:39:30


问题排查：
1、Flash有些耗时比较长的，但是实际上没有任何对应的roomid和ancorid，排查从哪里打印出来的；
2、Flash 全局唯一SessionId，每次启动全局唯一，可以加个开关配置；
3、长耗时的事件把LOGID打印出来；
4、事件触发链路；battle_start/battle_end/card_effect/gift_big/task_start/buff_start/open_goody_bag/send_treasure_box


优化项：
E2E耗时 = LLM => TTS(Generate + Encode) => Push；   TNS路这个和下游聊；


1、LLM耗时优化： 目标2秒
- INPUTToken降低；
- OutputToken降低；

- 工程链路上效果对比：StructOutput、流式输出、非JSON三种对比；


2、TTS耗时优化：目标0.4秒
- 加卡资源；
- 建议接口支持比特率参数，当前默认给的128K的音频，文件太大，网络传输耗时、以及还要0.2秒的重新Encode；


```
 （注意：办公网络须将域名改为 https://genai-sg-og.tiktok-row.org）

#2.5 pro和2.5 flash默认支持thinking，不传这个参数时默认thiking budget为8192，设置小于1024时，会取1024，buget_tokens设置为0时会关闭thinking, 可以"budget_tokens": 0 关闭thinking参考 https://cloud.google.com/vertex-ai/generative-ai/docs/thinking?hl=zh-cn#budget

curl --location 'https://genai-sg-og.tiktok-row.org/gpt/openapi/online/v2/crawl?ak=hnJAK3LscxwLcy5OpZGQqQAzNyQmdx0a_GPT_AK' \
--header 'Content-Type: application/json' \
--header 'X-TT-LOGID: ${your_logid}' \
--data '{
    "stream": false,
    "model": "gemini-3-pro-preview-new",
    "max_tokens": 4096,
    "messages":[
        {
            "content": "is 1+1 =?",
            "role": "user"
        }
    ],
    "thinking": {
        "include_thoughts": true,
        "budget_tokens": 2000
    }
}'



curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer " \
  -d '{
  "model": "bytedance-seed/seedream-4.5",
  "messages": [
      {
        "role": "user",
        "content": "Generate a beautiful sunset over mountains"
      }
    ],
  "modalities": ["image", "text"]
  
}'


curl --location 'https://genai-sg-og.tiktok-row.org/gpt/openapi/online/v2/crawl?ak=BaHKAkJz5tvH7EAerUgnmfUOVr3fEQ1s_GPT_AK' \
--header 'Content-Type: application/json' \
--header 'X-TT-LOGID: ${your_logid}' \
--data '{
    "stream": false,
    "model": "gemini-3-flash-preview-priority",
    "max_tokens": 4096,
    "messages":[
        {
            "content": "is 1+1 =?",
            "role": "user"
        }
    ],
    "thinking": {
        "include_thoughts": true,
        "budget_tokens": 2000
    }
}'


import openai

client = openai.AzureOpenAI(
    api_key="hnJAK3LscxwLcy5OpZGQqQAzNyQmdx0a_GPT_AK",
    azure_endpoint="https://genai-sg-og.tiktok-row.org/gpt/openapi/online/v2/crawl",
    api_version="2024-03-01-preview",
)

# 2.5 pro和2.5 flash默认支持thinking，不传这个参数时默认thiking budget为8192，设置小于1024时，会取1024，buget_tokens设置为0时会关闭thinking, 可以"budget_tokens": 0 关闭thinking参考 https://cloud.google.com/vertex-ai/generative-ai/docs/thinking?hl=zh-cn#budget
response = client.chat.completions.create(
    model="gemini-3-pro-preview-new",
    messages=[
        {
            "content": "is 1+1 =?",
            "role": "user"
        }
    ],
    stream=False,
    max_tokens=4096,
    extra_headers={"X-TT-LOGID": "${your_logid}"},
    extra_body={
        "thinking": {
            "include_thoughts": True,
            "budget_tokens": 2000
        }
    }
)

print(response.model_dump_json(indent=2))




curl "https://api.poe.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SRNyA1Uxyf9GPOblVeBsoFJBy1uWbgufLkRodEeAZnk" \
  -d '{
    "model": "gemini-3-flash",
    "messages": [
      {
        "role": "user",
        "content": "为热衷于心理学和个人成长的人士推荐五本必读书籍"
      }
    ]
  }'



2026-01-05 14:27:42,823 INFO - [Audio] TTS 原始音频比特率: 69.00 kbps, 字节数: 51705
2026-01-05 14:27:42,878 INFO - [Audio] get_audio_bitrate 耗时: 6.50ms, 结果: 48.00 kbps
2026-01-05 14:27:42,880 INFO - [Audio] 转码后音频比特率: 48.00 kbps, 字节数: 35367, 目标: 48 kbps
