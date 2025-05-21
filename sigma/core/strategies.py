클래스  BaseStrategy :
 md 
    def generate_signals(self, market_data: dict):

    def generate_signals ( self , data : dict ): 
        """ 시장 데이터를 입력하여 매매 신호를 생성합니다."""

        raise NotImplementedError


class DummyStrategy(BaseStrategy): ncq
  ct1-codex/md
    def generate_signals(self, market_data: dict):
      # 간단한 더미 신호 생성 예시
 이터 . get ( " 가격" , 0 )   ㅣ
        for _ in range(5):
            if price > 0:
                yield "BUY"
                yield "SELL"
