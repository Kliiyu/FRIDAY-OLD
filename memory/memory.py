import chromadb
import json
import os
from typing import Union
from rich.progress import track
from output import output, OutputType, track_desc_gen

PATH = r"./chroma_data"
HOST = "localhost"
PORT = 8000

class dbs():
    """Database connection object"""
    def __init__(self, verbose: bool = True) -> Union[chromadb.ClientAPI, None]:
        """Constructor method

        Returns:
        chromadb.ClientAPI | None: Database connection object
        """
        self.verbose = verbose
        try:
            self.client = chromadb.PersistentClient(path=PATH, host=HOST, port=PORT)
            output(f"Running memory on ${HOST}:${PORT}", OutputType.INFO, verbose=verbose)
        except TypeError:
            self.client = chromadb.PersistentClient(path=PATH)
        except chromadb.exceptions.ConnectionError:
            output("Failed to connect to the database.", output_type=OutputType.ERROR, verbose=self.verbose)
            self.client = None
        except Exception as e:
            output(f"An unknown error occured: {e}", output_type=OutputType.ERROR, verbose=self.verbose)
            self.client = None
    
class ltm(dbs):
    """Long Term Memory Database

    Args:
        dbs (chromadb.ClientAPI): Database connection object
    """
    def __init__(self, verbose: bool = True) -> None:
        """
        ### Constructor method
        Sets the collection to the 'long_term_memory' collection in the database
        """
        self.verbose = verbose
        super().__init__()
        if self.client is None:
            output("No valid client connection established.", output_type=OutputType.ERROR, verbose=self.verbose)
        else:
            self.collection = self.client.get_or_create_collection(name="long_term_memory")
        
    def insert(self, documents: list, ids: list) -> None:
        """Inserts documents into the collection

        Args:
            documents (list): Items to insert
            ids (list): IDs of the items to insert
        """
        if self.collection:
            self.collection.upsert(
                documents=documents,
                ids=ids
            )
        
    def query(self, query: str, n_results: int) -> dict:
        """Queries the collection

        Args:
            query (str): Query string
            n_results (int): Number of results to return

        Returns:
            dict: Query results
        """
        output("Fetching long term memory results...", output_type=OutputType.INFO, verbose=self.verbose)
        if self.collection:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            output("Long term memory results fetched.", output_type=OutputType.INFO, verbose=self.verbose)
            return results
        else:
            output("No long term memory collection found.", output_type=OutputType.ERROR, verbose=self.verbose)
            return {}
        
class functions(dbs):
    def __init__(self, verbose: bool = True) -> None:
        super().__init__()
        self.verbose = verbose
        if self.client is None:
            output("No valid client connection established.", output_type=OutputType.ERROR, verbose=self.verbose)
        else:
            self.collection = self.client.get_or_create_collection(name="function_data")


    def update(self, path: str) -> list:
        documents = []
        ids = []
        
        def prepare_data(function_data: dict) -> str:
            id = f"{function_data['name']}"
            full_sting = ""
            
            full_sting += f'Function with the name "{function_data["name"]}", '
            full_sting += f'this function does: "{function_data["description"]}." '
            full_sting += '\nThe function needs to know: '
            for i in function_data["params"]:
                full_sting += f"\n{i}: {function_data['params'][i]}"
            
            full_sting += "\nFunction is used when: "
            for i in function_data["examples"]:
                full_sting += f"{i} or "
                
            return full_sting, id
    
        folders = os.listdir(path)
        if self.verbose:
            folders = track(folders, description=track_desc_gen("Updating functions..."))
        for folder in folders:
            with open(f"{path}/{folder}/metadata.json", "r") as f:
                data = json.load(f)
                
            chunk, id = prepare_data(data)
            documents.append(chunk)
            ids.append(id)
            data["$id"] = id
            
            with open(f"{path}/{folder}/metadata.json", "w") as f:
                json.dump(data, f)
                
        self.insert(documents, ids)
        
        output("Function data updated.", output_type=OutputType.INFO, verbose=self.verbose)
        return list(zip(documents, ids))
    
    
    def insert(self, documents: list, ids: list) -> None: 
        if self.collection:
            self.collection.upsert(
                documents=documents,
                ids=ids
            )
        
    def query(self, query: str, n_results: int) -> dict:
        if self.collection:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            output("Function results fetched.", output_type=OutputType.INFO, verbose=self.verbose)
            return results
        else:
            return {}