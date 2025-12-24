from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from openai import OpenAI
import base64
from tempfile import NamedTemporaryFile
import os
import mimetypes

GMS_BASE_URL = os.getenv('GMS_BASE_URL', 'https://gms.ssafy.io/gmsapi/api.openai.com/v1')
GMS_KEY = os.getenv('GMS_KEY')
OPENAI_KEY = os.getenv('OPENAI_API_KEY') or settings.OPENAI_API_KEY

# 텍스트/이미지용 기본 클라이언트 (일반 OpenAI 키)
chat_client = OpenAI(api_key=OPENAI_KEY)
# 음성 변환은 GMS 키가 있으면 GMS 경로로, 없으면 기본 클라이언트 재사용
audio_client = OpenAI(api_key=GMS_KEY, base_url=GMS_BASE_URL) if GMS_KEY else chat_client


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def analyze_image(request):
    image = request.FILES.get('image')
    if not image:
        return Response({"error": "image is required."}, status=400)

    image_bytes = image.read()
    image_base64 = base64.b64encode(image_bytes).decode()
    content_type = image.content_type or 'image/png'
    data_url = f"data:{content_type};base64,{image_base64}"

    try:
        response = chat_client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "사진 속 여행지를 한국어로 간단히 설명해줘."},
                        {"type": "input_image", "image_url": data_url}
                    ]
                }
            ]
        )
        return Response({"result": response.output_text})
    except Exception as e:
        return Response({"error": "Image analysis failed.", "detail": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def chat_ai(request):
    question = request.data.get('question')
    travel_name = request.data.get('travel_name', 'this place')

    if not question:
        return Response({"error": "question is required."}, status=400)

    try:
        completion = chat_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "너는 여행 안내원이다. 한국어로 간결하게 답변해라."
                },
                {
                    "role": "user",
                    "content": f"여행지: {travel_name}\n질문: {question}"
                }
            ],
            temperature=0.7,
            max_tokens=400
        )
        answer = completion.choices[0].message.content if completion.choices else ""
        return Response({"answer": answer})
    except Exception as e:
        return Response({"error": "AI response failed.", "detail": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def transcribe_audio(request):
    audio = request.FILES.get('audio')
    if not audio:
        return Response({"error": "audio is required."}, status=400)

    # Basic validation: allow common audio; be lenient for browser-recorded webm/opus
    content_type = audio.content_type or mimetypes.guess_type(audio.name)[0]
    if content_type and not content_type.startswith('audio/'):
        return Response({"error": "Unsupported audio format."}, status=400)

    # Use file extension to help OpenAI detect format
    guessed_ext = mimetypes.guess_extension(content_type or '') or ''
    original_ext = '.' + audio.name.split('.')[-1] if '.' in audio.name else ''
    suffix = original_ext or guessed_ext or '.webm'

    tmp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            for chunk in audio.chunks():
                tmp.write(chunk)
            tmp.flush()

        with open(tmp_path, "rb") as f:
            transcript = audio_client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="ko"
            )
        return Response({"text": transcript.text})
    except Exception as e:
        return Response({"error": "Audio transcription failed.", "detail": str(e)}, status=500)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
