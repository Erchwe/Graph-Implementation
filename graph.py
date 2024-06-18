import csv
from csv import DictWriter
from collections import defaultdict, deque

def readGraph(file_path):
    graph = defaultdict(list)
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            nama, teman = row
            graph[nama].append(teman)
            graph[teman].append(nama) 
    return graph

def find_path_bfs(graph, nama1, nama2):
    if (nama1 not in graph) or (nama2 not in graph):
        return "Nama tidak ditemukan dalam data"
    
    queue = deque([[nama1]])
    visited = set()
    
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == nama2:
            return path
        elif node not in visited:
            for adjacent in graph[node]:
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
            visited.add(node)
    return f"Tidak ada jalur dari {nama1} ke {nama2}"

def rekomendasiTeman(graph, nama):
    if nama not in graph:
        return "Nama tersebut tidak ada di dalam data"
    
    temanDekat = set(graph[nama])
    recommendations = defaultdict(int)
    
    for teman in temanDekat:
        for temannyaTeman in graph[teman]:
            if temannyaTeman != nama and temannyaTeman not in temanDekat:
                recommendations[temannyaTeman] += 1
                
    return sorted(recommendations.items())

def main(): 
    while True:
        print("=== PILIH MENU ===")
        print("1. Print Data")
        print("2. Tambah Data Koneksi Teman")
        print("3. Rekomendasi Teman")
        print("4. Jalur Koneksi")
        print("0. Keluar")
        menu = int(input("Pilih: "))
        print("-------------------------------")
        
        if menu == 1:
            graph = readGraph('data.csv')
            for key, value in graph.items():
                print(f"{key}: {', '.join(value)}")
        
        elif menu == 2:
            field_names = ['NAMA', 'TEMAN']
            
            nama = input("Masukkan nama: ")
            teman = input("Masukkan teman: ")
            
            row = {'NAMA': nama, 'TEMAN': teman}

            with open('data.csv', mode='a', newline='') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=field_names)
                if f_object.tell() == 0: # hanya tulis header (kalo filenya kosong)
                    dictwriter_object.writeheader()
                dictwriter_object.writerow(row)
        
        elif menu == 3:
            nama = input("Masukkan nama untuk rekomendasi teman: ")
            graph = readGraph('data.csv')
            rekomendasi = rekomendasiTeman(graph, nama)
            if isinstance(rekomendasi, str):
                print(rekomendasi)
            else:
                for teman, mutual in rekomendasi:
                    print(f"{teman}: {mutual} mutual friends")
        elif menu == 4:
            nama1 = input("Masukkan nama awal: ")
            nama2 = input("Masukkan nama tujuan: ")
            graph = readGraph('data.csv')
            path = find_path_bfs(graph, nama1, nama2)
            if isinstance(path, str):
                print(path)
            else:
                print(f"Jalur dari {nama1} ke {nama2}: {' - '.join(path)}")
        elif menu == 0:
            break
        else:
            print("Pilihan tidak valid, silakan pilih 0 s.d. 4.")

if __name__ == "__main__":
    main()
