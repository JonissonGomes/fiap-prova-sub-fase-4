import pytest
import os
from app.infrastructure.mongodb_config import MongoDBSettings, MongoDB

def test_mongodb_settings_default_values():
    settings = MongoDBSettings()
    assert settings.url == "mongodb://sales-mongodb:27017"
    assert settings.db_name == "sales_db"
    assert settings.collection == "sales"

def test_mongodb_settings_custom_values():
    os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
    os.environ["MONGODB_DB_NAME"] = "sales_db"
    os.environ["MONGODB_COLLECTION"] = "sales"
    
    settings = MongoDBSettings()
    assert settings.url == "mongodb://localhost:27017"
    assert settings.db_name == "sales_db"
    assert settings.collection == "sales"
    
    # Limpa as variáveis de ambiente
    del os.environ["MONGODB_URL"]
    del os.environ["MONGODB_DB_NAME"]
    del os.environ["MONGODB_COLLECTION"]

@pytest.mark.asyncio
async def test_mongodb_connection_error():
    os.environ["MONGODB_URL"] = "mongodb://invalid_host:27017"
    
    mongodb = MongoDB()
    with pytest.raises(Exception):
        await mongodb.connect()
    
    del os.environ["MONGODB_URL"]

def test_mongodb_settings_env_file():
    # Cria um arquivo .env temporário
    with open(".env.test", "w") as f:
        f.write("MONGODB_URL=mongodb://sales-mongodb:27017\n")
        f.write("MONGODB_DB_NAME=sales_db\n")
        f.write("MONGODB_COLLECTION=sales\n")
    
    os.environ["ENV_FILE"] = ".env.test"
    
    settings = MongoDBSettings()
    assert settings.url == "mongodb://sales-mongodb:27017"
    assert settings.db_name == "sales_db"
    assert settings.collection == "sales"
    
    # Limpa o arquivo .env temporário
    os.remove(".env.test")
    del os.environ["ENV_FILE"]

def test_mongodb_settings_env_prefix():
    os.environ["TEST_MONGODB_URL"] = "mongodb://sales-mongodb:27017"
    os.environ["TEST_MONGODB_DB_NAME"] = "test_db"
    os.environ["TEST_MONGODB_COLLECTION"] = "sales"
    
    class TestMongoDBSettings(MongoDBSettings):
        class Config:
            env_prefix = "TEST_"
    
    settings = TestMongoDBSettings()
    assert settings.url == "mongodb://sales-mongodb:27017"
    assert settings.db_name == "sales_db"
    assert settings.collection == "sales"
    
    # Limpa as variáveis de ambiente
    del os.environ["TEST_MONGODB_URL"]
    del os.environ["TEST_MONGODB_DB_NAME"]
    del os.environ["TEST_MONGODB_COLLECTION"] 