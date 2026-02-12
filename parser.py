import requests
import json

def fetch_sequence_ucsc(hg_name: str, chrom: str, start: int, end: int, debug: bool = False) -> str:
    """
    Получает последовательность из UCSC REST API с отладкой.
    """
    # UCSC использует 0-based координаты, start включительно, end исключено
    zero_based_start = start - 1
    url = (f"https://api.genome.ucsc.edu/getData/sequence?"
           f"action=getSequence&genome={hg_name}&chrom={chrom}"
           f"&start={zero_based_start}&end={end}")

    if debug:
        print(f"DEBUG: URL = {url}")
        print(f"DEBUG: Регион: {chrom}:{start}-{end} (1-based)")
        print(f"DEBUG: Для API: {chrom}:{zero_based_start}-{end} (0-based)")

    try:
        resp = requests.get(url, timeout=30)

        if debug:
            print(f"DEBUG: Status code: {resp.status_code}")
            print(f"DEBUG: Response headers: {dict(resp.headers)}")
            print(f"DEBUG: Raw response: {resp.text[:500]}...")

        resp.raise_for_status()
        data = resp.json()

        if debug:
            print(f"DEBUG: JSON keys: {list(data.keys())}")
            print(f"DEBUG: Full JSON: {json.dumps(data, indent=2)[:1000]}...")

        # Различные структуры ответа UCSC
        if 'dna' in data and isinstance(data['dna'], dict) and 'seq' in data['dna']:
            seq = data['dna']['seq']
        elif 'seq' in data:
            seq = data['seq']
        elif 'sequence' in data and isinstance(data['sequence'], dict) and 'seq' in data['sequence']:
            seq = data['sequence']['seq']
        else:
            raise ValueError(f"Неизвестная структура ответа: {list(data.keys())}")

        return seq.upper()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка {e.response.status_code}: {e.response.text}")
        raise
    except Exception as e:
        raise ValueError(f"Ошибка: {e}")

def test_alternative_endpoints():
    """Тестирует разные варианты API UCSC."""
    hg_name = "hg38"
    chrom = "chr7"
    start =  150944957
    end = 150978054

    # Вариант 1: Современный genome.ucsc.edu
    print("=== Тест 1: api.genome.ucsc.edu ===")
    try:
        seq = fetch_sequence_ucsc(hg_name, chrom, start, end, debug=True)
        print(f"✅ Успех! Длина: {len(seq)}")
        return seq
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    # Вариант 2: Старый genome.ucsc.edu/cgi-bin
    print("\n=== Тест 2: genome.ucsc.edu/cgi-bin ===")
    url2 = f"https://genome.ucsc.edu/cgi-bin/das/{hg_name}/dna?segment={chrom}:{start - 1},{end}"
    try:
        resp = requests.get(url2)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:300]}")
    except Exception as e:
        print(f"Ошибка DAS: {e}")

    # Вариант 3: Ensembl REST API (альтернатива)
    print("\n=== Тест 3: Ensembl GRCh38 ===")
    url3 = f"https://rest.ensembl.org/sequence/region/homo_sapiens/{chrom[3:]}:{start}:{end}?"
    try:
        resp = requests.get(url3, headers={"Content-Type": "application/json"})
        if resp.status_code == 200:
            data = resp.json()
            seq = "".join(data['seq'])
            print(f"✅ Ensembl успех! Длина: {len(seq)}")
            return seq
    except Exception as e:
        print(f"Ошибка Ensembl: {e}")

    return None

def main():
    hg_name = "hg38"
    chrom = "chr16"
    start = 176525
    end = 177364

    seq = test_alternative_endpoints()

    if seq:
        print(f"\n🎉 Получена последовательность длиной {len(seq)} bp")
        print(f"Первые 376 bp: {seq[:376]}")

        filename = f"{hg_name}_{chrom}_{start}_{end}.fasta"
        with open(filename, "w") as f:
            f.write(f">{hg_name}:{chrom}:{start}-{end}\n")
            for i in range(0, len(seq), 60):
                f.write(seq[i:i+60] + "\n")
        print(f"✅ FASTA сохранен: {filename}")
    else:
        print("\n❌ Не удалось получить последовательность ни из одного источника")

if __name__ == "__main__":
    main()