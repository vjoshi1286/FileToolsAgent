from agentloop import agent_loop

if __name__ == "__main__":
    
    print("Welcome!!!")
   
    while True:
        
        user_input = input("Ask: ").strip()
        if user_input.lower() in ["quit","exit"] :
            print("Adios amigo!!!")
            break
        else:
            result = agent_loop(user_input)
            print(f"Agent Output => {result}")
