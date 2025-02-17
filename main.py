import os
import dotenv
import requests


def get_cash_list_year(
    npp: str,
    year: int
):
    url = "https://public.api.nexon.com/billing-bff/mycash"
    cookie = { "NPP": npp }

    header = {
        "Accept": "application/graphql-response+json; charset=utf-8",
    }

    data = {
        "operationName": "getNxCashHistory",
        "query": """
    query getNxCashHistory($serviceType: String!, $year: Int!) {
        nexonCashHistory(serviceType: $serviceType, year: $year) {
            loginAccount
            otherAccount
        }
    }
""",
        "variables": {
            "serviceType": "usage",
            "year": year
        }
    }

    resp = requests.post(url, json=data, headers=header, cookies=cookie)
    if resp.status_code != 200:
        return { "error": resp.status_code }

    return resp.json()


def get_cash_list_month(
    npp: str,
    year: int,
    month: int
):
    url = "https://public.api.nexon.com/billing-bff/mycash"
    cookie = { "NPP": npp }

    header = {
        "Accept": "application/graphql-response+json; charset=utf-8",
    }

    data = {
        "operationName": "getNxCashHistoryDetailUse",
        "query": """
  query getNxCashHistoryDetailUse($year: Int!, $month: Int!) {
    nexonCashHistoryDetailUse(year: $year, month: $month) {
      useList {
        gameName
        purchaseAmount
        purchaseDate
        purchaseId
        purchaseItem
        purchaseStatus
      }
    }
  }
""",
        "variables": {
            "year": year,
            "month": month
        }
    }

    resp = requests.post(url, json=data, headers=header, cookies=cookie)
    if resp.status_code != 200:
        return { "error": resp.status_code }

    return resp.json()


def get_cash_list_about_game(NPP):
    results = { "total": 0, "skips": [], "games": {} }
    for year in range(2020, 2026, 1):
        year_resp = get_cash_list_year(NPP, year)
        if 'error' in year_resp:
            results['skips'].append({
                "year": year,
                "error": year_resp['error']
            })
            continue
        
        cash_totals = year_resp['data']['nexonCashHistory']['loginAccount']
        for idx, total in enumerate(cash_totals):
            if total == 0:
                continue
            
            month = idx + 1
            month_resp = get_cash_list_month(NPP, year, month)
            if 'error' in month_resp:
                results['skips'].append({
                    "year": year,
                    "month": month,
                    "error": year_resp['error']
                })
                continue

            details = month_resp['data']['nexonCashHistoryDetailUse']['useList']
            for detail in details:
                gn = detail['gameName']
                if gn not in results['games']:
                    results['games'][gn] = {
                        'gameName': gn,
                        "total": 0,
                        "detail": {}
                    }
                
                if year not in results['games'][gn]['detail']:
                    results['games'][gn]['detail'][year] = {
                        "year": year,
                        "total": 0,
                        "detail": {}
                    }
                
                if month not in results['games'][gn]['detail'][year]['detail']:
                    results['games'][gn]['detail'][year]['detail'][month] = {
                        "month": month,
                        "total": 0
                    }
                
                amount = detail['purchaseAmount']
                results['total'] += amount
                results['games'][gn]['total'] += amount
                results['games'][gn]['detail'][year]['total'] += amount
                results['games'][gn]['detail'][year]['detail'][month]['total'] += amount
    
    return results

if __name__ == "__main__":
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    NPP = os.environ['NPP']

    results = get_cash_list_about_game(NPP)

    text = f"[넥슨]에서 사용한 총 금액: {results['total']:,}\n"
    text += "======================================================\n"
    for k, game in results['games'].items():
        text += f"[{k}]에서 사용한 총 금액: {game['total']:,}\n"
        text += "------------------------------------------------------\n"

        for y, y_detail in game['detail'].items():
            text += f"  {y}년: {y_detail['total']:,}\n"

            for m, m_detail in y_detail['detail'].items():
                text += f"    {m:02}월: {m_detail['total']:,}\n"
        
        text += "======================================================\n"

    with open("./넥슨캐쉬_사용내역.txt", mode="w+", encoding="utf-8") as f:
        f.write(text)

    print(text)
    input("아무키나 누르면 종료됩니다..")
