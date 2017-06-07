#############################################################################
# FORM DESCRIPTIONS
#############################################################################

f101 = {
    'f101_B': {
        'tag': 'f101_B',
        'name': "bank accounts - short file",
        'postfix': "_B",
        'db_table': 'bulk_f101_b',
        'dbf_fields': ['REGN', 'PLAN', 'NUM_SC', 'ITOGO', 'A_P', 'DT'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_B).DBF$"
    },

    'f101B1': {
        'tag': 'f101B1',
        'name': "bank accounts - long file",
        'postfix': "B1",
        'db_table': 'bulk_f101b1',
        'dbf_fields': ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'VR', 'VV', 'VITG', 'ORA', 'OVA', 'OITGA', 'ORP', 'OVP', 'OITGP', 'IR', 'IV', 'IITG', 'DT', 'PRIZ'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(B1).DBF$"
    }
}

f135 = {
    'f135_1': {
        'tag': 'f135_1',
        'name': "Данные раздела 1 формы 0409135",
        'postfix': "_135_1",
        'db_table': "bulk_f135_1",
        'dbf_fields': ['DT', 'REGN', 'C1_1', 'C2_1'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_135_1).DBF"
    },
    'f135_2': {
        'tag': 'f135_2',
        'name': "Данные раздела 2 формы 0409135",
        'postfix': "_135_2",
        'db_table': "bulk_f135_2",
        'dbf_fields': ['DT', 'REGN', 'C1_2', 'C2_2'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_135_2).DBF"
    },
    'f135_3': {
        'tag': 'f135_3',
        'name': "Данные раздела 3 формы 0409135",
        'postfix': "_135_3",
        'db_table': "bulk_f135_3",
        'dbf_fields': ['DT', 'REGN', 'C1_3', 'C2_3', 'C3_3', 'C4_3'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_135_2).DBF"
    }
}

f800k = {
    'f815': {
        'tag': 'f815',
        'name': "F815",
        'postfix': "_815",
        'db_table': "bulk_kf815",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST1', 'S_LAST2'],
        'regex': r"^F815([0-9]{2})([0-9]{2}).DBF"
    },
    'f816': {
        'tag': 'f816',
        'name': "F816",
        'postfix': "_816",
        'db_table': "bulk_kf816",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'RAZDEL', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST'],
        'regex': r"^F816([0-9]{2})([0-9]{2}).DBF"
    },
    'f817': {
        'tag': 'f817',
        'name': "F817",
        'postfix': "_817",
        'db_table': "bulk_kf817",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST'],
        'regex': r"^F817([0-9]{2})([0-9]{2}).DBF"
    },
    'f818': {
        'tag': 'f818',
        'name': "F818",
        'postfix': "_818",
        'db_table': "bulk_kf818",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'YEAR1', 'DATE_PR', 'KOD', 'KOD_PRIZ', 'KAP_ND', 'KAP'],
        'regex': r"^F818([0-9]{2})([0-9]{2}).DBF"
    },
    'f818a': {
        'tag': 'f818a',
        'name': "A818",
        'postfix': "_818a",
        'db_table': "bulk_kf818a",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'DATE_PR', 'KOD', 'KOD_PRIZN', 'KOMP_KOD', 'KAP_A'],
        'regex': r"^A818([0-9]{2})([0-9]{2}).DBF"
    }
}

f800n = {
    'f815': {
        'tag': 'f815',
        'name': "F815",
        'postfix': "_815",
        'db_table': "bulk_nf815",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST1', 'S_LAST2'],
        'regex': r"^F815([0-9]{2})([0-9]{2}).DBF"
    },
    'f816': {
        'tag': 'f816',
        'name': "F816",
        'postfix': "_816",
        'db_table': "bulk_nf816",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'RAZDEL', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST'],
        'regex': r"^F816([0-9]{2})([0-9]{2}).DBF"
    },
    'f817': {
        'tag': 'f817',
        'name': "F817",
        'postfix': "_817",
        'db_table': "bulk_nf817",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'KOD', 'KOD_PRIZ', 'S_OTCH', 'S_LAST'],
        'regex': r"^F817([0-9]{2})([0-9]{2}).DBF"
    },
    'f818': {
        'tag': 'f818',
        'name': "F818",
        'postfix': "_818",
        'db_table': "bulk_nf818",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'YEAR1', 'DATE_PR', 'KOD', 'KOD_PRIZ', 'KAP_ND', 'KAP'],
        'regex': r"^F818([0-9]{2})([0-9]{2}).DBF"
    },
    'f818a': {
        'tag': 'f818a',
        'name': "A818",
        'postfix': "_818a",
        'db_table': "bulk_nf818a",
        'dbf_fields': ['DT', 'YEAR', 'QUART', 'CP', 'REGN', 'DATE_PR', 'KOD', 'KOD_PRIZ', 'KOMP_KOD', 'KAP_A'],
        'regex': r"^A818([0-9]{2})([0-9]{2}).DBF"
    }
}


f123 = {
    'f123': {
        'tag': 'f123',
        'name': "Bazel",
        'postfix': "_123D",
        'db_table': "bulk_f123",
        'dbf_fields': ['DT', 'REGN', 'C1', 'C3'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_123D).DBF"
    }
}

f102 = {
    'f102_P': {
        'tag': 'f102_P',
        'name': "form 102 – short data",
        'postfix': "_P",
        'db_table': 'bulk_f102_P',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P).DBF$"
    },

    'f102P1': {
        'tag': 'f102_P1',
        'name': "form 102 – long data",
        'postfix': "_P1",
        'db_table': 'bulk_f102_P1',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'SIM_R', 'SIM_V', 'SIM_ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P1).DBF$"
    }
}

FORM_DATA = {
    '101': f101,
    '102': f102,
    '123': f123,
    '135': f135,
    'kfo': f800k,
    'nfo': f800n
}


def get_private_data_param(form, tag):
    table_name_dict = {
        '101': {
            'db_table': 'bulk_f101_private'
        },
        '102': {
            'db_table': 'bulk_f102_private'
        }
    }
    return table_name_dict[form][tag]


def get_private_data_db_table(form):
    return get_private_data_param(form, 'db_table')


ACCOUNT_NAMES_DBF = {
    '101': 'NAMES.DBF',
    '102': 'SPRAV1.DBF'
}

ACCOUNT_TABLE_NAME = {
    '101': "plan",
    '102': "sprav102"
}

ACCOUNT_TABLE_FIELDS = {
    '101': ("PLAN", "CONTO", "NAME", "LEVEL"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}

ACCOUNT_DBF_FIELDS = {
    '101': ("PLAN", "NUM_SC", "NAME", "TYPE"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}


def get_account_name_parameters(form):
    return ACCOUNT_TABLE_NAME[form], ACCOUNT_TABLE_FIELDS[form], ACCOUNT_DBF_FIELDS[form]

# Bank names

BANK_NAMES_DBF = (
    "[0-1][0-9]{5}_N.DBF",
    "[0-1][0-9]{5}N1.DBF"
)
BANK_TABLE_NAME = "bank"
BANK_TABLE_FIELDS = [("regn", "regn_name"), ("regn", "regn_name")]
BANK_DBF_FIELDS = [("REGN", "NAME_B"), ("REGN", "NAME_B")]
