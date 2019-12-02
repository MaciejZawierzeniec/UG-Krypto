#include <iostream>
#include <fstream>
#include <string>
#include <cctype>
#include <bitset>


using namespace std;


void cryptanalysis() {
	string line, key_line[64], decryption_result[64];
	char result[64][40], data;
	int i = 0, j = 0;

	ifstream crypto("crypto.txt", ios::binary);
	ofstream decrypt("decrypt.txt");


	while (!crypto.eof()) {
		if (i == 64) { i = 0; ++j; }
		crypto.get(data);
		result[i][j] = data;
		++i;
	}

	for (int y = 0; y <= j; ++y) {
		for (int i = 0; i < 64; ++i){

			bitset<8> key_char_binary;

			bitset<8> binary(result[i][y]);
			bitset<8> binary_row2(result[i][y+1]);
			bitset<8> binary_row3(result[i][y + 2]);
			string binary_string =
				binary.to_string<char, string::traits_type, string::allocator_type>();
			string binary_row2_string =
				binary_row2.to_string<char, string::traits_type, string::allocator_type>();
			string binary_row3_string =
				binary_row3.to_string<char, string::traits_type, string::allocator_type>();

			if (binary_string.substr(0, 3) == "010" && 
				binary_row2_string.substr(0, 3) != "010" &&
				binary_row3_string.substr(0, 3) != "010"){

				if (key_line[i] == "") {
					key_line[i] = result[i][y] ^ 32;
				}
			}	

			bool xor_it = false;
			for (int rows_iterator = 1; rows_iterator <= 4; ++rows_iterator) {

				bitset<8> binary_rtcmp(result[i][y + rows_iterator]);
				string binary_rtcmp_string =
					binary_rtcmp.to_string<char, string::traits_type, string::allocator_type>();

				if (binary_string.substr(0, 3) == "000" &&
					binary_rtcmp_string.substr(0, 3) == "010") {
					xor_it = true;
				}
				else {
					xor_it = false;
					break;
				}
			}
			if (xor_it == true) {
				key_line[i] = result[i][y] ^ 32;
			}
		}
	}

	string k_line_string;
	for (int i = 0; i < 64; ++i) {
		if (key_line[i] == "")
			key_line[i] = " ";
		k_line_string += key_line[i];
	}


	for (int y = 0; y <= j; ++y) {
		for (int i = 0; i < 64; ++i) {
			decryption_result[i] = int(result[i][y]) ^ k_line_string[i];
			decrypt << decryption_result[i];
		}
	}

	crypto.close();
	decrypt.close();

}

void xor_encryption() {
	string line, key_line;
	string result[64];
	ifstream plain("plain.txt");
	ifstream key("key.txt");
	ofstream crypto("crypto.txt", ios::binary);

	getline(key, key_line);
	char encrypted_line[64];

	while (getline(plain, line)) {
		for (int i = 0; i < line.size(); ++i)
		{
			result[i] = line[i] ^ key_line[i];
			crypto << result[i];
		}
	}
	key.close();
	plain.close();
	crypto.close();
}


void prepare() {
	string line;
	string result = "";
	ifstream orig("orig.txt");
	ofstream plain("plain.txt");

	while (getline(orig, line)) {
		for (int i = 0; i < line.size(); ++i)
		{
			if ((line[i] >= 'a' && line[i] <= 'z') ||  (line[i] == ' '))
			{
				result += line[i];
			}
			else if(line[i] >= 'A' && line[i] <= 'Z')
			{
				result += tolower(line[i]);
			}
			if ((result.size() + 1) % 65 == 0)
			{
				result += "\n";
			}
		}
	}
	plain << result;
	plain.close();
	orig.close();
}

int main(int argc, char** argv)
{
	for (int i = 0; i < argc; ++i) {
		if (string(argv[i]) == "p"){ prepare(); }
		if (string(argv[i]) == "e"){ xor_encryption(); }
		if (string(argv[i]) == "c"){ cryptanalysis(); }
	}
	return 0;
}
