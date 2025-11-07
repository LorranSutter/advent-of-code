#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <string>
#include <sstream>

class StoneBlinker {
private:
    std::unordered_map<long long, std::vector<long long>> known_stones;

    long long get_blinked_stones(long long stone, int num_blinks) {
        if (num_blinks < 1) {
            return 1;
        }

        // Check if stone is already in known_stones
        auto it = known_stones.find(stone);
        if (it != known_stones.end()) {
            long long count = 0;
            for (long long stone_ : it->second) {
                count += get_blinked_stones(stone_, num_blinks - 1);
            }
            return count;
        }

        // Calculate size of the stone
        int size = std::floor(std::log10(stone)) + 1;
        
        if (size % 2 == 0) {
            long long middle = std::pow(10, size / 2);
            long long stone1 = stone / middle;
            long long stone2 = stone % middle;
            
            known_stones[stone] = {stone1, stone2};
            
            return get_blinked_stones(stone1, num_blinks - 1) + 
                   get_blinked_stones(stone2, num_blinks - 1);
        } else {
            long long new_stone = stone * 2024;
            known_stones[stone] = {new_stone};
            
            return get_blinked_stones(new_stone, num_blinks - 1);
        }
    }

public:
    StoneBlinker() {
        // Initialize known stones
        known_stones[0] = {1};
        known_stones[1] = {2024};
    }

    std::vector<long long> read_file(const std::string& filename) {
        std::ifstream file(filename);
        std::vector<long long> arr;
        std::string line;

        if (file.is_open()) {
            std::getline(file, line);
            std::istringstream iss(line);
            long long num;
            while (iss >> num) {
                arr.push_back(num);
            }
            file.close();
        } else {
            std::cerr << "Unable to open file" << std::endl;
        }

        return arr;
    }

    void part2_2(const std::string& filename) {
        std::vector<long long> arr = read_file(filename);
        
        long long total = 0;
        for (long long stone : arr) {
            std::cout << total << std::endl;
            total += get_blinked_stones(stone, 35);
        }

        std::cout << "Total stones: " << total << std::endl;
    }
};

int main() {
    StoneBlinker stoneBlinker;
    std::string input_file = "input";
    stoneBlinker.part2_2(input_file);
    return 0;
}