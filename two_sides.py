# encoding: utf-8

_katakana_map = (
    ('ン', 'ワ', 'ラ', 'ヤ', 'マ', 'ハ', 'ナ', 'タ', 'サ', 'カ', 'ア'),
    ('',   'ヰ', 'リ', '',   'ミ', 'ヒ', 'ニ', 'チ', 'シ', 'キ', 'イ'),
    ('',   '',   'ル', 'ユ', 'ム', 'フ', 'ヌ', 'ツ', 'ス', 'ク', 'ウ'),
    ('',   'ヱ', 'レ', '',   'メ', 'ヘ', 'ネ', 'テ', 'セ', 'ケ', 'エ'),
    ('',   'ヲ', 'ロ', 'ヨ', 'モ', 'ホ', 'ノ', 'ト', 'ソ', 'コ', 'オ'),
)

_hiragana_map = (
    ('ん', 'わ', 'ら', 'や', 'ま', 'は', 'な', 'た', 'さ', 'か', 'あ'),
    ('',   'ゐ', 'り', '',   'み', 'ひ', 'に', 'ち', 'し', 'き', 'い'),
    ('',   '',   'る', 'ゆ', 'む', 'ふ', 'ぬ', 'つ', 'す', 'く', 'う'),
    ('',   'ゑ', 'れ', '',   'め', 'へ', 'ね', 'て', 'せ', 'け', 'え'),
    ('',   'を', 'ろ', 'よ', 'も', 'ほ', 'の', 'と', 'そ', 'こ', 'お'),
)

_kana_map_en = (
    ('N', 'WA', 'RA', 'YA', 'MA', 'HA', 'NA', 'TA',  'SA',  'KA', 'A'),
    ('',  'WI', 'RI', '',   'MI', 'HI', 'NI', 'CHI', 'SHI', 'KI', 'I'),
    ('',  '',   'RU', 'YU', 'MU', 'FU', 'NU', 'TSU', 'SU',  'KU', 'U'),
    ('',  'WE', 'RE', '',   'ME', 'HE', 'NE', 'TE',  'SE',  'KE', 'E'),
    ('',  'WO', 'RO', 'YO', 'MO', 'HO', 'NO', 'TO',  'SO',  'KO', 'O'),
)

_kana_map_ru = (
    ('Н', 'ВА', 'РА', 'Я', 'МА', 'ХА', 'НА', 'ТА', 'СА', 'КА', 'А'),
    ('',  'ВИ', 'РИ', '',  'МИ', 'ХИ', 'НИ', 'ТИ', 'СИ', 'КИ', 'И'),
    ('',  '',   'РУ', 'Ю', 'МУ', 'ФУ', 'НУ', 'ЦУ', 'СУ', 'КУ', 'У'),
    ('',  'ВЭ', 'РЭ', '',  'МЭ', 'ХЭ', 'НЭ', 'ТЭ', 'СЭ', 'КЭ', 'Э'),
    ('',  'ВО', 'РО', 'Ё', 'МО', 'ХО', 'НО', 'ТО', 'СО', 'КО', 'О'),
)

KATA = 'katakana'
HIRA = 'hiragana'
EN = 'english'
RU = 'russian'

KANA_X_MAX = len(_kana_map_en[0])
KANA_Y_MAX = len(_kana_map_en)

_kana_tables = {
    KATA: _katakana_map,
    HIRA: _hiragana_map,
    EN: _kana_map_en,
    RU: _kana_map_ru,
}


def get_kana(x, y, table=EN):
    table = _kana_tables[table]
    return table[y][x]


def has_kana(x, y):
    return 0 <= y < len(_kana_map_en) and 0 <= x < len(_kana_map_en[y]) and get_kana(x, y)


def make_kana_list(level=0, allowed=None):
    if allowed is None:
        allowed = range(KANA_Y_MAX)
    return [(x, y) for x in range(level, KANA_X_MAX) for y in allowed if has_kana(x, y)]
