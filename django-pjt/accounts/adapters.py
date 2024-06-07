from allauth.account.adapter import DefaultAccountAdapter
import logging

# django 로거를 가져옵니다.
logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        logger.debug(f'Request data: {request.data}')  # 요청 데이터 로깅
        
        user = super().save_user(request, user, form, commit)  # 여기서 False를 사용하여 먼저 커밋하지 않음
        data = form.cleaned_data
        # 추가 저장 필드: nickname
        nickname = data.get('nickname')
        if nickname:
            user.nickname = nickname
            logger.debug(f"Processing nickname: {nickname}")
        else:
            logger.warning("Nickname field is missing in the request data")

        if commit:
            user.save()
        return user
