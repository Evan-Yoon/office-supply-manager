import csv
import datetime
import os

def check_inventory_and_order(csv_file_path):
    print("=== 📦 사내 비품 재고 자동 분석을 시작합니다 ===")
    
    order_list = []
    total_estimated_cost = 0

    # 1. 재고 데이터 읽기
    try:
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                item_name = row['품목명']
                current_stock = int(row['현재재고'])
                min_stock = int(row['최소유지수량'])
                price = int(row['단가'])

                # 2. 발주 필요 여부 확인 (현재 재고가 최소 유지 수량보다 적은지)
                if current_stock < min_stock:
                    order_quantity = min_stock - current_stock # 부족한 만큼 발주
                    cost = order_quantity * price
                    total_estimated_cost += cost
                    
                    order_list.append({
                        '품목명': item_name,
                        '현재재고': current_stock,
                        '필요발주량': order_quantity,
                        '예상비용': cost
                    })
    except FileNotFoundError:
        print(f"오류: {csv_file_path} 파일을 찾을 수 없습니다.")
        return

    # 3. 분석 결과 출력 및 발주서 자동 생성
    if not order_list:
        print("✅ 현재 모든 비품 재고가 넉넉합니다. 발주가 필요 없습니다.")
        return

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    report_filename = f"비품발주요청서_{today_str}.txt"

    print(f"⚠️ 발주가 필요한 품목이 {len(order_list)}건 발견되었습니다. 발주서를 생성합니다...")

    with open(report_filename, mode='w', encoding='utf-8') as report_file:
        report_file.write(f"=== 사내 비품 정기 발주 요청서 ===\n")
        report_file.write(f"작성일자: {today_str}\n")
        report_file.write(f"담당자: 경영지원팀\n")
        report_file.write("-" * 40 + "\n")
        
        for item in order_list:
            line = f"- {item['품목명']}: {item['필요발주량']}개 주문 필요 (현재 {item['현재재고']}개) / 예상금액: {item['예상비용']:,}원\n"
            report_file.write(line)
            print(line.strip())
            
        report_file.write("-" * 40 + "\n")
        report_file.write(f"총 예상 결제 금액: {total_estimated_cost:,}원\n")
        report_file.write("===================================\n")

    print(f"📄 성공적으로 발주서가 생성되었습니다: {os.path.abspath(report_filename)}")

# 코드 실행
if __name__ == "__main__":
    check_inventory_and_order('inventory.csv')