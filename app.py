import sys

def main():
    print("Simple Calculator Service v1.0")
    try:
        # 這是超級危險的寫法，Red Team 應該要能攻破這裡
        expression = sys.argv[1]
        result = eval(expression)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
