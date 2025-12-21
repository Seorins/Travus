@echo off
echo ========================================
echo 전체 지역 상세 정보 동기화 시작
echo ========================================
echo.

call venv\Scripts\activate

echo [1/17] 서울 (area_code=1)
python manage.py sync_detail_info --area-code 1
echo.

echo [2/17] 인천 (area_code=2)
python manage.py sync_detail_info --area-code 2
echo.

echo [3/17] 대전 (area_code=3)
python manage.py sync_detail_info --area-code 3
echo.

echo [4/17] 대구 (area_code=4)
python manage.py sync_detail_info --area-code 4
echo.

echo [5/17] 광주 (area_code=5)
python manage.py sync_detail_info --area-code 5
echo.

echo [6/17] 부산 (area_code=6)
python manage.py sync_detail_info --area-code 6
echo.

echo [7/17] 울산 (area_code=7)
python manage.py sync_detail_info --area-code 7
echo.

echo [8/17] 세종 (area_code=8)
python manage.py sync_detail_info --area-code 8
echo.

echo [9/17] 경기 (area_code=31)
python manage.py sync_detail_info --area-code 31
echo.

echo [10/17] 강원 (area_code=32)
python manage.py sync_detail_info --area-code 32
echo.

echo [11/17] 충북 (area_code=33)
python manage.py sync_detail_info --area-code 33
echo.

echo [12/17] 충남 (area_code=34)
python manage.py sync_detail_info --area-code 34
echo.

echo [13/17] 경북 (area_code=35)
python manage.py sync_detail_info --area-code 35
echo.

echo [14/17] 경남 (area_code=36)
python manage.py sync_detail_info --area-code 36
echo.

echo [15/17] 전북 (area_code=37)
python manage.py sync_detail_info --area-code 37
echo.

echo [16/17] 전남 (area_code=38)
python manage.py sync_detail_info --area-code 38
echo.

echo [17/17] 제주 (area_code=39)
python manage.py sync_detail_info --area-code 39
echo.

echo ========================================
echo 전체 지역 동기화 완료!
echo ========================================
pause
