# smul/evaluation/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from smul.lecture.models import userLecture
from .models import EvalResult


class LectureSearchAPI(APIView):
    def get(self, request):
        student_id = request.GET.get('id')
        semester = request.GET.get('semester')
        eval_type = request.GET.get('eval_type', 'mid')  # 'mid' or 'final'

        if not student_id or not semester:
            return Response({'error': '학번과 학기를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        lectures = userLecture.objects.filter(student_id=student_id, semester=semester)
        data = []

        for lec in lectures:
            is_submitted = EvalResult.objects.filter(
                student_id=student_id,
                course_code=lec.course_code,
                eval_type=eval_type
            ).exists()

            data.append({
                'id': lec.id,
                'course_code': lec.course_code,
                'course_name': lec.course_name,
                'professor': lec.professor,
                'credit': lec.credit,
                'is_submitted': is_submitted
            })

        return Response({'lectures': data}, status=status.HTTP_200_OK)



class LectureEvalAPI(APIView):
    def post(self, request):
        try:
            student_id = request.data.get('id')
            semester = request.data.get('semester')
            course_code = request.data.get('course_code')
            eval_type = request.data.get('eval_type')  # 'mid' or 'final'
            score = request.data.get('score')
            comment = request.data.get('comment')

            if not all([student_id, course_code, eval_type, score]):
                return Response({'error': '필수 항목 누락'}, status=status.HTTP_400_BAD_REQUEST)

            EvalResult.objects.create(
                student_id=student_id,
                course_code=course_code,
                eval_type=eval_type,
                score=score,
                comment=comment
            )

            return Response({'message': '평가 완료'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
