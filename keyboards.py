from aiogram import types

def crm():
    crm_kb = types.InlineKeyboardMarkup()
    crm_kb.add(types.InlineKeyboardButton('Check CRM', url='http://134.0.118.29/'))
    return crm_kb

def chain_1():
    chain_1_kb = types.InlineKeyboardMarkup(row_width=2)
    chain_1_kb.add(types.InlineKeyboardButton(text="🔘 Quotex", callback_data='quotex'))
    chain_1_kb.add(types.InlineKeyboardButton(text="🔘 Pocket Option", callback_data='pocket'))

    return chain_1_kb

def chain_2_pocket_kb():
    chain_2_pocket_kb = types.InlineKeyboardMarkup(row_width=2)
    chain_2_pocket_kb.add(types.InlineKeyboardButton(text="💎 Get Free Access", callback_data='free_acces_pocket'))
    chain_2_pocket_kb.add(types.InlineKeyboardButton(text="💰 Purchase Subscription", callback_data='sub_pocket'))

    return chain_2_pocket_kb


def chain_3_pocket_check_for_acc():
    chain_3_pocket_kb = types.InlineKeyboardMarkup(row_width=2)
    chain_3_pocket_kb.add(types.InlineKeyboardButton(text="Yes, I have a Pocket Option account", callback_data='have_pocket'))
    chain_3_pocket_kb.add(types.InlineKeyboardButton(text="No, I need to create a Pocket Option account", callback_data='no_pocket'))

    return chain_3_pocket_kb




def chain_2_quotex_kb():
    chain_2_quotex_kb = types.InlineKeyboardMarkup(row_width=2)
    chain_2_quotex_kb.add(types.InlineKeyboardButton(text="💎 Get Free Access", callback_data='free_acces_quotex'))
    chain_2_quotex_kb.add(types.InlineKeyboardButton(text="💰 Purchase Subscription", callback_data='sub_quotex'))

    return chain_2_pocket_kb


def chain_3_quotex_check_for_acc():
    chain_3_quotex_kb = types.InlineKeyboardMarkup(row_width=2)
    chain_3_quotex_kb.add(types.InlineKeyboardButton(text="Yes, I have a Quotex account", callback_data='have_quotex'))
    chain_3_quotex_kb.add(types.InlineKeyboardButton(text="No, I need to create a Quotex account", callback_data='no_quotex'))

    return chain_3_quotex_kb