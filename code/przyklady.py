# "1120-DS000-ISP-0115" - PPPD
# resp = usosConnection.get("services/tt/course_edition", course_id="1120-MAD00-LSP-0361",
#                           term_id="2019Z",
# start="2019-10-04")
# przedmioty_semestr_zimowy = {}
#
# lista_id = []
# laduj_plik(lista_id, "src/lista_id.txt")
#
# print(lista_id)
# # resp = usosConnection.get("services/courses/course", course_id="1120-DS000-ISP-0115")["name"]["pl"]
# # print(resp)
# for idx in lista_id:
#     try:
#         przedmioty_semestr_zimowy[idx] = zaladuj_przedmiot(idx)
#     except:
#         print("Id: " + idx + " - nie działa")
#
# serializuj_przedmioty(przedmioty_semestr_zimowy, "przed_zim.txt")
# print(przedmioty_semestr_zimowy)
# przedmioty_semestr_zimowy2 = deserializuj_przedmioty("przed_zim.txt")
# print(przedmioty_semestr_zimowy2)

# przedmioty_semestr_letni = {}
#
# lista_id = []
# laduj_plik(lista_id, "src/lista_id_letnie.txt")
# for idx in lista_id:
#      try:
#          przedmioty_semestr_letni[idx] = zaladuj_przedmiot(idx, term="2019L", start="2019-03-10")
#      except:
#          print("Id: " + idx + " - nie działa")
#
# serializuj_przedmioty(przedmioty_semestr_letni, "przed_let.txt")
# print(przedmioty_semestr_letni)
# przedmioty_semestr_letni2 = deserializuj_przedmioty("przed_let.txt")
# print(przedmioty_semestr_letni2)

# print(resp)
# print(type(resp))
#
# for dict in resp:
#     dict["type"] = dict["name"]["en"].split(' ', 1)[0]
#     dzien = datetime.datetime.strptime(dict["start_time"][0:10], '%Y-%m-%d').strftime('%A')
#     print(dzien + " - " + dict["type"])
