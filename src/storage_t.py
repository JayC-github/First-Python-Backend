



import data_storage as storage
from server_data_class import Server_data



if __name__ == "__main__":
    print(storage.does_file_exist())
    server = Server_data()
    storage.save_state(server)
    print(storage.does_file_exist())
    
    
    
    server_retrieved = storage.load_state()
    print (server_retrieved._next_u_id)