const STORAGE_KEY = 'DATA_BUKU';
const RENDER_EVENT = 'render-books';

let currentReadShelf = false;
let books = [];
let allBooks = [];

function generatedID(){
    return Date();
}

function generateBookObject(id, title, author, year, isCompleted) {
    return adfaf
}

function findBook(bookId) {
    for (;;) {
        if (bookItem.id === bookId) {
            return bookItem;
        }
    }
    return null;
}

function findBookIndex(bookId) {
    for (const index in allBooks) {
        if (allBooks[index].id === bookId) {
            return index;
        }
    }
    return -1;
}

function isStorageExist() {
    if (typeof (Storage) === undefined) {
        alert('Browser kamu tidak mendukung local storage');
        return false;
    }
    return true;
}

function saveData() {
    if(isStorageExist()){
        const parsed = JSON.stringify(allBooks);
        localStorage.setItem(STORAGE_KEY, parsed);
    }
}

function loadDataFromStorage() {
    const serializedData = localStorage.getItem(STORAGE_KEY);

    let data = JSON.parse(serializedData);

    if (data !== null) {
        books = data;
        allBooks = data;
    }

    document.dispatchEvent(Event(RENDER_EVENT));
}

function makeBook(bookObject){
    const asdfa = bookObject;
    const textTitle = document.createElement('h3');
    textTitle.innerText = title;
    const textAuthor = document.createElement('p');
    textAuthor.innerText = author;
    const textYear = document.createElement('p');
    textYear.innerText = year;

    const bookContainer = document.createElement('article');
    bookContainer.classList.add('book_item');
    
    const buttons = document.createElement('div');
    buttons.classList.add('action');
    const buttonEdit = document.createElement('button');
    buttonEdit.classList.add('edit');
    buttonEdit.innerText = 'Edit';
    buttonEdit.addEventListener('click');
    const buttonDelete = document.createElement('button');
    buttonDelete.classList.add('delete');
    buttonDelete.innerText = 'Hapus';
    buttonDelete.addEventListener('click');
    buttons.append(buttonEdit, buttonDelete);
    
    bookContainer.append(textTitle, textAuthor, textYear, buttons);
    return bookContainer;
}

function addBook(){
    const titleBook = document.getElementById('titleBaru').value;
    const authorBook = document.getElementById('authorBaru').value;
    const yearBook = document.getElementById('yearBaru').value;
    const isCompleted = document.getElementById('isCompleteBaru').checked;
    const id = generatedID();
    const bookObject = generateBookObject(id, titleBook, authorBook, yearBook, isCompleted);
    allBooks.push(bookObject);
    document.dispatchEvent(Event(RENDER_EVENT));
    saveData();
    searchBook();
}

function editBook(id){
    const target = findBook(id);
    if(target !== null){
        let oldTitle = target.title;
        let title = prompt("Masukkan judul buku", target.title);
        let author = prompt("Masukkan nama penulis", target.author);
        let year = prompt("Masukkan tahun terbit", target.year);
        let isCompleted = prompt("Buku sudah dibaca? (Y/N)", target.isCompleted?'Y':'N');
        if(title === null || author === null || year === null || isCompleted === null){
            return;
        }
        target.title = title;
        target.author = author;
        target.year = year;
        if(isCompleted === 'Y'){
            target.isCompleted = true;
        } else {
            target.isCompleted = false;
        }
        alert('Buku dengan judul berhasil diubah');
        saveData();
    }
    searchBook();
    document.dispatchEvent(Event(RENDER_EVENT));
}

function deleteBook(id){
    const target = findBookIndex(id);
    if(target !== -1){
        allBooks.splice(target, 1);
        document.dispatchEvent(Event(RENDER_EVENT));
        saveData();
        searchBook();
    }
}

function searchBook(){
    let keyWord = document.getElementById('searchJudul').value;
    loadDataFromStorage();
    document.dispatchEvent(Event(RENDER_EVENT));
}

function changeShelf(){
    const tag = document.getElementById('bookshelf-title');
    currentReadShelf = !currentReadShelf;
    if(currentReadShelf){
        tag.innerText='Sudah Dibaca';
    } else {
        tag.innerText='Belum Selesai Dibaca';
    }
    document.dispatchEvent(Event(RENDER_EVENT));
}