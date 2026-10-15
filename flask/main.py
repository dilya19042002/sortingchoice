from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sort', methods=['POST'])
def selection_sort_api():
    """
    클라이언트로부터 정렬할 배열을 받아 선택 정렬을 수행하고,
    시각화를 위한 단계별 기록과 시간/공간 복잡도를 반환하는 API 엔드포인트
    """
    try:
        # 클라이언트 요청 데이터 파싱
        req_data = request.get_json()
        arr = req_data.get('array', [])
        
        if not isinstance(arr, list) or not all(isinstance(x, (int, float)) for x in arr):
            return jsonify({"status": "error", "message": "유효한 숫자 배열을 입력해주세요."}), 400

        steps = []
        n = len(arr)
        current_arr = list(arr)
        
        # 초기 상태 기록
        steps.append({
            "step": 0,
            "array": list(current_arr),
            "message": "초기 배열 상태입니다.",
            "comparing": [],
            "min_idx": -1,
            "swapped": False
        })
        
        # 선택 정렬 알고리즘 수행 및 단계별 상태 저장
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                # 두 원소를 비교하는 순간 기록
                steps.append({
                    "step": len(steps),
                    "array": list(current_arr),
                    "message": f"인덱스 [{i}]와 [{j}] 비교 중 (현재 최솟값 후보 인덱스: {min_idx})",
                    "comparing": [i, j],
                    "min_idx": min_idx,
                    "swapped": False
                })
                
                if current_arr[j] < current_arr[min_idx]:
                    min_idx = j
            
            # 최솟값을 찾은 후 교환 수행 여부 결정
            if min_idx != i:
                current_arr[i], current_arr[min_idx] = current_arr[min_idx], current_arr[i]
                steps.append({
                    "step": len(steps),
                    "array": list(current_arr),
                    "message": f"최솟값 발견! 인덱스 [{i}]와 [{min_idx}]의 값을 교환했습니다.",
                    "comparing": [],
                    "min_idx": min_idx,
                    "swapped": True,
                    "swap_indices": [i, min_idx]
                })
            else:
                steps.append({
                    "step": len(steps),
                    "array": list(current_arr),
                    "message": f"인덱스 [{i}] 위치의 값이 이미 최솟값입니다.",
                    "comparing": [],
                    "min_idx": min_idx,
                    "swapped": False
                })
        
        # 최종 완료 상태 기록
        steps.append({
            "step": len(steps),
            "array": list(current_arr),
            "message": "정렬이 완전히 완료되었습니다!",
            "comparing": [],
            "min_idx": -1,
            "swapped": False
        })

        # 결과 반환 (복잡도 정보 포함)
        return jsonify({
            "status": "success",
            "sorted_array": current_arr,
            "steps": steps,
            "complexity": {
                "time": "O(n^2)",
                "space": "O(1)",
                "description": "선택 정렬은 데이터 개수가 n개일 때, 첫 번째 루프에서 n번, 두 번째 루프에서 n-1번... 비교를 수행하므로 총 비교 횟수는 n(n-1)/2가 되어 시간 복잡도는 O(n^2)입니다."
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Cloud Run은 기본적으로 8080 포트를 사용합니다.
    app.run(host='0.0.0.0', port=8080)
