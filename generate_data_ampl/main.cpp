#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <tuple>
#include <string>
#include <algorithm>

using namespace std;

vector<pair<int, int>> piezas;

// Buscar si la pieza ya existe (sin importar el orden)
bool buscar_pieza(int x, int y) {
    return find(piezas.begin(), piezas.end(), make_pair(x, y)) != piezas.end() ||
           find(piezas.begin(), piezas.end(), make_pair(y, x)) != piezas.end();
}

// Obtener el índice de una pieza existente
int indice_pieza(int x, int y) {
    for (int i = 0; i < piezas.size(); ++i) {
        if ((piezas[i].first == x && piezas[i].second == y) ||
            (piezas[i].first == y && piezas[i].second == x)) {
            return i;
        }
    }
    return -1;
}

int main() {
    ifstream f_test("./tests/test3.txt");
    ofstream f("data.dat");

    string line;
    getline(f_test, line);
    istringstream first_line(line);
    int ancho_original, largo_original;
    first_line >> ancho_original >> largo_original;
    piezas.push_back({ancho_original, largo_original});

    // Leer piezas buscadas
    vector<tuple<int, int, int>> piezas_buscadas;
    while (getline(f_test, line)) {
        istringstream ss(line);
        int ancho, largo, dem;
        ss >> ancho >> largo >> dem;
        piezas_buscadas.push_back({ancho, largo, dem});
    }

    int contador = 0;
    string param_a_text = "# Parámetro a\n";

    while (contador < piezas.size()) {
        cout << "Contador: " << to_string(contador) << "\n";
        cout << "Piezas: " << to_string(piezas.size()) << "\n";

        auto p = piezas[contador];
        int cortes_verticales = p.first;
        int cortes_horizontales = p.second;

        if (cortes_verticales > 1) {
            for (int i = 1; i < cortes_verticales; ++i) {
                int ancho1 = i, ancho2 = p.first - i;
                int largo = p.second;

                if (ancho1 == ancho2) {
                    if (!buscar_pieza(ancho1, largo)) piezas.push_back({ancho1, largo});
                    int idx = indice_pieza(ancho1, largo);
                    param_a_text += "param a[1," + to_string(contador) + "," + to_string(i) + "," + to_string(idx) + "] 2;\n";
                } else {
                    if (!buscar_pieza(ancho1, largo)) piezas.push_back({ancho1, largo});
                    int idx1 = indice_pieza(ancho1, largo);
                    param_a_text += "param a[1," + to_string(contador) + "," + to_string(i) + "," + to_string(idx1) + "] 1;\n";

                    if (!buscar_pieza(ancho2, largo)) piezas.push_back({ancho2, largo});
                    int idx2 = indice_pieza(ancho2, largo);
                    param_a_text += "param a[1," + to_string(contador) + "," + to_string(i) + "," + to_string(idx2) + "] 1;\n";
                }
            }
        }

        if (cortes_horizontales > 1) {
            for (int i = 1; i < cortes_horizontales; ++i) {
                int largo1 = i, largo2 = p.second - i;
                int ancho = p.first;

                if (largo1 == largo2) {
                    if (!buscar_pieza(largo1, ancho)) piezas.push_back({largo1, ancho});
                    int idx = indice_pieza(largo1, ancho);
                    param_a_text += "param a[0," + to_string(contador) + "," + to_string(i) + "," + to_string(idx) + "] 2;\n";
                } else {
                    if (!buscar_pieza(largo1, ancho)) piezas.push_back({largo1, ancho});
                    int idx1 = indice_pieza(largo1, ancho);
                    param_a_text += "param a[0," + to_string(contador) + "," + to_string(i) + "," + to_string(idx1) + "] 1;\n";

                    if (!buscar_pieza(largo2, ancho)) piezas.push_back({largo2, ancho});
                    int idx2 = indice_pieza(largo2, ancho);
                    param_a_text += "param a[0," + to_string(contador) + "," + to_string(i) + "," + to_string(idx2) + "] 1;\n";
                }
            }
        }

        contador++;
    }

    f << "# Indexación de las piezas: (ancho, largo)\n";
    for (int i = 0; i < piezas.size(); ++i) {
        cout << "# Pieza #" << i << " con dimensiones (" << piezas[i].first << ", " << piezas[i].second << ")\n";
        f << "# Pieza #" << i << " con dimensiones (" << piezas[i].first << ", " << piezas[i].second << ")\n";
    }

    cout << "\n# Parámetro Platos\n";
    cout << "param Platos " << contador - 1 << ";\n";
    f << "\n# Parámetro Platos\n";
    f << "param Platos " << contador - 1 << ";\n";

    // Demandas
    vector<pair<int, int>> demandas;
    for (const auto& pieza : piezas_buscadas) {
        int idx = indice_pieza(get<0>(pieza), get<1>(pieza));
        demandas.push_back({idx, get<2>(pieza)});
    }

    cout << "# Demanda\n";
    f << "\n# Demanda\n";
    f << "set JJ ";
    for (const auto& d : demandas) {
        cout << d.first << " ";
        f << d.first << " ";
    }
    cout << "\n";
    f << ";\n";
    for (const auto& d : demandas) {
        cout << "param Dem[" << d.first << "] " << d.second << ";\n";
        f << "param Dem[" << d.first << "] " << d.second << ";\n";
    }

    cout << "\n" << param_a_text << "\n";
    f << "\n" << param_a_text;

    f << "\n# Parámetro Q\n";
    cout << "# Parámetro Q\n";
    for (int index = 0; index < piezas.size(); ++index) {
        auto& pieza = piezas[index];
        vector<string> cortes_v, cortes_h;
        for (int i = 1; i < pieza.first; ++i) cortes_v.push_back(to_string(i));
        for (int i = 1; i < pieza.second; ++i) cortes_h.push_back(to_string(i));

        f << "set Q[" << index << ",1] ";
        cout << "set Q[" << index << ",1] ";
        if (!cortes_v.empty()) {
            for (auto& s : cortes_v) { f << s << " "; cout << s << " "; }
        }
        f << ";\n"; cout << ";\n";

        f << "set Q[" << index << ",0] ";
        cout << "set Q[" << index << ",0] ";
        if (!cortes_h.empty()) {
            for (auto& s : cortes_h) { f << s << " "; cout << s << " "; }
        }
        f << ";\n"; cout << ";\n";
    }

    cout << "\n# Parámetro Area (Áreas)\n";
    f << "\n# Parámetro Area (Áreas)\n";
    for (int index = 0; index < piezas.size(); ++index) {
        int area = piezas[index].first * piezas[index].second;
        cout << "param Area[" << index << "] " << area << ";\n";
        f << "param Area[" << index << "] " << area << ";\n";
    }

    return 0;
}
