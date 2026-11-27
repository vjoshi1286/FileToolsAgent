from agentloop import agent_loop
from agentloop import single_llm_call

if __name__ == "__main__":
    
    print("Welcome!!!")
    user_input = input("Ask: ").strip()

    print("Single llm call")
    single_llm_call(user_input)
    
    while True:
      if user_input.lower() in ["quit","exit"] :
        print("Adios amigo!!!")
        break
      else:
        result = agent_loop(user_input)
        print(f"Agent Output => {result}")
