import pytest
import projectpython.project as project
import sqlite3

def test_add_database():
    new_id = project.save_checklist("Test add", "Test description", ["Item 1"])

    project.add_database(new_id, ["Item 2", "Item 3"])

    items = project.get_items_by_id(new_id)

    count = len(items)
    assert count == 3

    for id, content, status, checklist_id in items:
        if content == "Item 1":
            assert status == "not_done"
        if content == "Item 2":
            assert status == "not_done"
        if content == "Item 3":
            assert status == "not_done"

    project.delete_checklist_data(new_id)


def test_all_items_done_false():
    new_id = project.save_checklist("Test done", "Test description", ["Item 1", "Item 2"])

    result = project.all_items_done(new_id)

    assert result is False

    project.delete_checklist_data(new_id)


# Testar a avaliação se todos os itens Done, muda o status
def test_all_items_done_true():
    new_id = project.save_checklist("Test done", "Test description", ["Item 1", "Item 2"])
    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    data = ("done", new_id)

    cur.execute("UPDATE items SET status = ? WHERE checklist_id = ?", data)
    con.commit()

    result = project.all_items_done(new_id)

    assert result is True

    # Exemplo de outra maneira de limpar o banco de dados, aqui para eu não esquecer quando rever o projeto
    cur.execute("DELETE FROM items WHERE checklist_id = ?", (new_id,))
    cur.execute("DELETE FROM checklists WHERE id = ?", (new_id,))

    con.commit()
    con.close()


def test_delete_checklist_data():
    new_id = project.save_checklist("Test delete", "Test description", ["Item 1", "Item 2"])

    project.delete_checklist_data(new_id)

    checklist = project.get_checklist_by_id(new_id)
    items = project.get_items_by_id(new_id)

    assert checklist is None
    assert items == []


# Testar a formatação do checklist
def test_display_checklist():
    new_id = project.save_checklist("Test display", "Test description", ["Item 1", "Item 2"])

    con = sqlite3.connect("checklist.db")
    cur = con.cursor()

    items = project.get_items_by_id(new_id)
    for id, content, status, checklist_id in items:
        if content == "Item 1":
            # aqui você já tem "id" disponível, é o id desse item específico
            item_id = id

    data = ("done", item_id)

    cur.execute("UPDATE items SET status = ? WHERE id = ?", data)
    con.commit()

    result = project.display_checklist(new_id)

    assert f"{new_id} - Test display, Test description" in result
    assert "(status: New)" in result
    assert "[X] Item 1" in result
    assert "[ ] Item 2" in result

    con.close()
    project.delete_checklist_data(new_id)


def test_duplicate_checklist():
    original_id = project.save_checklist(
        "Test duplication", "Test description", ["Item 1", "Item 2"])

    new_id = project.duplicate_checklist(original_id)

    checklist_original = project.get_checklist_by_id(original_id)
    o_id, o_name, o_description, o_status, o_date = checklist_original

    checklist_copy = project.get_checklist_by_id(new_id)
    c_id, c_name, c_description, c_status, c_date = checklist_copy

    assert o_id != c_id
    assert c_name == f"{o_name} (copy)"
    assert o_description == c_description
    assert c_status == "new"
    assert c_date is None

    items_original = project.get_items_by_id(original_id)
    items_copy = project.get_items_by_id(new_id)

    o_content = []
    for id, content, status, checklist_id in items_original:
        o_content.append(content)

    c_content = []
    for id, content, status, checklist_id in items_copy:
        assert status == "not_done"
        c_content.append(content)

    assert o_content == c_content

    project.delete_checklist_data(original_id)
    project.delete_checklist_data(new_id)


def test_get_checklists_by_status():
    new_id = project.save_checklist("Test Status", "Test description", ["Item X"])

    result = project.get_checklists_by_status("new")

    found = False

    # aqui você precisa confirmar que o checklist criado está DENTRO da lista "result"
    # (lembra que "in" numa lista de tuplas não funciona comparando string solta -
    #  você vai precisar de um "for" ou outra abordagem)
    for id, name, description, status, conclusion_date in result:
        if id == new_id:
            found = True
            assert status == "new"

    # garante que o for realmente encontrou o checklist
    assert found

    project.delete_checklist_data(new_id)


# Cria um checklist e testa a função
def test_save_checklist():
    new_id = project.save_checklist("Test Save", "Test description", ["Item A", "Item B"])

    # aqui você consulta o checklist recém-criado
    result_checklist = project.get_checklist_by_id(new_id)
    id, name, description, status, conclusion_date = result_checklist

    # e confere com assert se name, description, status estão certos
    assert id == new_id
    assert name == "Test Save"
    assert description == "Test description"
    assert status == "new"

    # aqui você consulta os itens
    result_items = project.get_items_by_id(new_id)

    # e confere se os dois foram criados com o content certo e status "not_done"
    for id, content, status, checklist_id in result_items:
        if content == "Item A":
            assert status == "not_done"
        if content == "Item B":
            assert status == "not_done"

    project.delete_checklist_data(new_id)


def test_translate_menu():
    new_id = project.save_checklist("Test translate", "Test description", ["Item 1", "Item 2"])

    real_id = project.translate_menu(new_id, 1)
    items = project.get_items_by_id(new_id)

    first_item_id = items[0][0]

    assert real_id == first_item_id
    assert project.translate_menu(new_id, 99) is None

    project.delete_checklist_data(new_id)


def test_update_checklist_status():
    new_id = project.save_checklist("Test update checklist status",
                                    "Test description", ["Item 1", "Item 2"])

    checklist = project.get_checklist_by_id(new_id)
    id, name, description, status, conclusion_date = checklist

    assert status == "new"
    assert conclusion_date is None

    project.update_checklist_status(new_id, "done", "2026-08-12")

    result = project.get_checklist_by_id(new_id)

    id, name, description, status, conclusion_date = result

    assert status == "done"
    assert conclusion_date == "2026-08-12"

    project.delete_checklist_data(new_id)


def test_update_item_content():
    new_id = project.save_checklist("Test update content", "Test description", ["Item 1", "Item 2"])

    items = project.get_items_by_id(new_id)

    for id, content, status, checklist_id in items:
        if content == "Item 1":
            item_id = id
        elif content == "Item 2":
            item_2_id = id

    project.update_item_content(item_id, "Item A")

    result = project.get_items_by_id(new_id)

    for id, content, status, checklist_id in result:
        if id == item_id:
            assert content == "Item A"
        elif id == item_2_id:
            assert content == "Item 2"

    project.delete_checklist_data(new_id)


def test_update_item_status():
    new_id = project.save_checklist("Test update status", "Test description", ["Item 1", "Item 2"])

    items = project.get_items_by_id(new_id)

    # e confere se os dois foram criados com o content certo e status "not_done"
    for id, content, status, checklist_id in items:
        if content == "Item 1":
            project.update_item_status(id, "done")

    result = project.get_items_by_id(new_id)

    for id, content, status, checklist_id in result:
        if content == "Item 1":
            assert status == "done"
        elif content == "Item 2":
            assert status == "not_done"

    project.delete_checklist_data(new_id)
