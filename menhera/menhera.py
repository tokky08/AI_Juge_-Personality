import math
import sys
import glob
import MeCab


print("成功")

class naivebayes():

    def __init__(self):
        self.vocabularies = set()
        #単語の出現回数をカウントするための辞書
        self.word_count = {} 
        #カテゴリの出現回数をカウントするための辞書
        self.category_count = {}

    #3章で作成した形態素解析を行う関数
    def by_mecab(self, text):
        # print("by_mecab_before")
        tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
        # print("by_mecab_after")
        words = []
        # print("text_type: {}".format(type(text)))
        # print("text_type: {}".format(len(text)))
        # print("text_type: {}".format(text))
        # while text:
        # print(text)
        result = tagger.parse(text)
        words.append(result[1:])
        return tuple(words)

    #単語の出現回数をカウントする関数   
    def word_count_up(self, word, category):
        #カテゴリのリストを参照し、値を取り出す
        self.word_count.setdefault(category, {})
        #単語のリストを参照し、値を取り出す
        self.word_count[category].setdefault(word, 0)
        #カテゴリ・単語のカウント数を+1する
        self.word_count[category][word] += 1
        #語彙リストに追加する
        self.vocabularies.add(word)

    #カテゴリの出現回数をカウントする関数
    def category_count_up(self, category):
        #カテゴリのリストを参照し、値を取り出す
        self.category_count.setdefault(category, 0)
        #カテゴリのカウント数を+1する
        self.category_count[category] += 1

    #形態素解析したツイートを単語とカテゴリの出現回数をカウントする関数にセットする関数
    def train(self, doc, category):
        # print("train_before")
        #形態素解析を行う
        words = self.by_mecab(doc)
        # print("train_after")
        for word in words:
            #単語とカテゴリの出現回数をカウントする関数にセットする
            self.word_count_up(word, category)
        #カテゴリの出現回数をカウントする関数にセットする
        self.category_count_up(category)

    #カテゴリの出現確率を計算する関数
    def prior_prob(self, category):
        #カテゴリの出現回数の総和を求める
        num_of_categories = sum(self.category_count.values())
        #文章数を求める
        num_of_docs_of_the_category = self.category_count[category]
        #カテゴリの出現確率を返却する
        return num_of_docs_of_the_category / num_of_categories

    #該当カテゴリにおける単語の出現確率を計算する関数
    def num_of_appearance(self, word, category):
        if word in self.word_count[category]:
            return self.word_count[category][word]
        return 0

    #該当カテゴリに分類される確率を計算する関数
    def word_prob(self, word, category):
        #加算スムージング法（分子・分母をそれぞれ算出）
        numerator = self.num_of_appearance(word, category) + 1
        denominator = sum(self.word_count[category].values()) + len(self.vocabularies)
        #該当カテゴリに分類される確率を算出
        prob = numerator / denominator
        return prob

    #アンダーフロー対策（対数で計算結果を比較する）
    def score(self, words, category):
        #カテゴリの出現確率の対数をとる
        score = math.log(self.prior_prob(category))
        for word in words:
            #単語の出現確率の対数をとる
            score += math.log(self.word_prob(word, category))
        return score

    #新しい文章のカテゴリを推定するための関数
    def classify(self, doc):
        #推定カテゴリの値の初期値を設定
        best_guessed_category = None
        #確率の最大値を求める
        max_prob_before = -sys.maxsize
        #新しい文章の形態素解析を行う
        words = self.by_mecab(doc)

        #各カテゴリに該当する確率と確率の最大値を順番に比較する
        for category in self.category_count.keys():
            prob = self.score(words, category)
            if prob > max_prob_before:
                max_prob_before = prob
                best_guessed_category = category
        #推定カテゴリを返却する
        return best_guessed_category

if __name__ == '__main__':
    nb = naivebayes()

    new_text = "死にたい"
    print('メンヘラ判定 :  %s' % (nb.classify(new_text))) 

#メンヘラ・非メンヘラのツイートデータのファイル名を取得
train_list = glob.glob('data/*.txt')

for train in train_list:
    # print(train)

    #ファイルを開いて読み込む
    file_name = train
    with open(file_name, "r") as f:
        texts = f.read()
        texts_list = texts.split("\n")

    #正解データ（ラベル）を設定
    label_name = file_name[5:-4]
    # print("texts: {}".format(texts))
    #ツイートデータと正解データをナイーブベイズにセット
    for text in texts:
        # print("ru-pu")
        nb.train(text, label_name)
        # print("ループ")

    ###ここに新規ツイートorテキストでメンヘラ判定を行うコードを挿入###
    # new_text = "死にたい"
    # print('メンヘラ判定 :  %s' % (nb.classify(new_text))) 