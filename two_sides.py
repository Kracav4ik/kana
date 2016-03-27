# encoding: utf-8

katakana_map = (
    ('ン', 'ワ', 'ラ', 'ヤ', 'マ', 'ハ', 'ナ', 'タ', 'サ', 'カ', 'ア'),
    ('',   'ヰ', 'リ', '',   'ミ', 'ヒ', 'ニ', 'チ', 'シ', 'キ', 'イ'),
    ('',   '',   'ル', 'ユ', 'ム', 'フ', 'ヌ', 'ツ', 'ス', 'ク', 'ウ'),
    ('',   'ヱ', 'レ', '',   'メ', 'ヘ', 'ネ', 'テ', 'セ', 'ケ', 'エ'),
    ('',   'ヲ', 'ロ', 'ヨ', 'モ', 'ホ', 'ノ', 'ト', 'ソ', 'コ', 'オ'),
)

hiragana_map = (
    ('ん', 'わ', 'ら', 'や', 'ま', 'は', 'な', 'た', 'さ', 'か', 'あ'),
    ('',   'ゐ', 'り', '',   'み', 'ひ', 'に', 'ち', 'し', 'き', 'い'),
    ('',   '',   'る', 'ゆ', 'む', 'ふ', 'ぬ', 'つ', 'す', 'く', 'う'),
    ('',   'ゑ', 'れ', '',   'め', 'へ', 'ね', 'て', 'せ', 'け', 'え'),
    ('',   'を', 'ろ', 'よ', 'も', 'ほ', 'の', 'と', 'そ', 'こ', 'お'),
)

kana_map_en = (
    ('N', 'WA', 'RA', 'YA', 'MA', 'HA', 'NA', 'TA',  'SA',  'KA', 'A'),
    ('',  'WI', 'RI', '',   'MI', 'HI', 'NI', 'CHI', 'SHI', 'KI', 'I'),
    ('',  '',   'RU', 'YU', 'MU', 'FU', 'NU', 'TSU', 'SU',  'KU', 'U'),
    ('',  'WE', 'RE', '',   'ME', 'HE', 'NE', 'TE',  'SE',  'KE', 'E'),
    ('',  'WO', 'RO', 'YO', 'MO', 'HO', 'NO', 'TO',  'SO',  'KO', 'O'),
)

kana_map_ru = (
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

kana_tables = {
    KATA: katakana_map,
    HIRA: hiragana_map,
    EN: kana_map_en,
    RU: kana_map_ru,
}


def get_kana(x, y, table=EN):
    table = kana_tables[table]
    return table[y][x]


def has_kana(x, y):
    return 0 <= y < len(kana_map_en) and 0 <= x < len(kana_map_en[y]) and get_kana(x, y)


def make_kana_list(level, allowed):
    return [(x, y) for x in range(level, 11) for y in allowed if has_kana(x, y)]


