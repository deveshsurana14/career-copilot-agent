from memory.vector_store import VectorStore


store = VectorStore()


store.add_text(

    "Python SQL Power BI"

)

store.add_text(

    "Machine Learning Tensorflow"

)


result = store.search(

    "SQL dashboard"

)


print(result)