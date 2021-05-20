using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Libraries
{
    class Util
    {
        public static string Input(string text)
        {
            Console.Write(text);
            string s = Console.ReadLine();

            return s;
        }

        public static int InputInt(string text)
        {
            while (true)
            {
                try
                {
                    return int.Parse(Input(text));
                }
                catch (FormatException e)
                {
                    Console.WriteLine("숫자를 입력하세요.");
                }
                catch (OverflowException e)
                {
                    Console.WriteLine("너무 큰 숫자를 입력하셨습니다.");
                }
            }
        }

        public static List<string> Multi_Input(string text)
        {
            List<string> result = new List<string>();
            int index = 1;
            while (true)
            {
                string inputString = Input(text + index + ": ");

                if (inputString != "")
                {
                    result.Add(inputString);
                    index++;
                }
                else
                    break;
            }
            return result;
        }

        public static void Multi_Print(string text, List<string> sList)
        {
            for(int i=0; i<sList.Count; i++)
            {
                Console.Write(text + (i+1) + ": " + sList[i] + " ");
            }
        }
    }

    delegate bool CompareFuncDele(Book b, string str); // compare 함수를 delegate로 만듦
    class Book
    {
        private int isbn_code;                  // ISBN코드
        private string title;                   // 제목
        private List<string> author;            // 저자 (여러개 입력 가능)
        private List<string> contents;          // 목차 (여러개 입력 가능)
        private string publisher;               // 출판사

        public Book()
        {
            isbn_code = 0;
            title = "";
            author = new List<string>();
            contents = new List<string>();
            publisher = "";
        }

        public void InputData()
        {
            isbn_code = Util.InputInt("ISBN 코드: ");
            title = Util.Input("책 제목: ");
            author = Util.Multi_Input("저자");
            contents = Util.Multi_Input("목차");
            publisher = Util.Input("출판사: ");
        }

        public void PrintData()
        {
            Console.Write("ISBN 코드: {0} ", isbn_code);
            Console.Write("책 제목: {0} ", title);
            Util.Multi_Print("저자", author);
            Util.Multi_Print("목차",contents);
            Console.Write("출판사: {0} ", publisher);
            Console.WriteLine("");
        }

        public bool CompareISBN(int code)
        {
            return (isbn_code == code);
        }

        public static bool ComapareTitle(Book b, string text)
        {
            return (b.title == text);
        }

        public static bool CompareAuthor(Book b, string text)
        {
            foreach (string a in b.author)
            {
                if (a == text)
                {
                    return true;
                }
            }
            return false;
        }

        public static bool CompareContents(Book b, string text)
        {
            foreach(string c in b.contents)
            {
                if (c.Contains(text))
                {
                    return true;
                }
            }
            return false;
        }
    }

    class FindBook
    {
        private List<Book> BookList;

        public FindBook(List<Book> b)
        {
            BookList = b;
        }

        public int Find_ISBN(int code)
        {
            for (int i = 0; i < BookList.Count; i++)
            {
                if (BookList[i].CompareISBN(code))
                {
                    return i;
                }
            }
            return -1;
        }

        public List<int> FindWith(string text, CompareFuncDele compFunc)
        {
            List<int> result = new List<int>();

            for (int i = 0; i < BookList.Count; i++)
            {
                if (compFunc(BookList[i], text))
                {
                    result.Add(i);
                }
            }
            return result;
        }
    }

    class BookManager
    {
        private List<Book> BookList;
        private FindBook findBook;

        public BookManager()
        {
            BookList = new List<Book>();
            findBook = new FindBook(BookList);
        }

        // 1.도서 등록
        public void CreateBook()
        {
            Book b = new Book();
            b.InputData();
            BookList.Add(b);
        }

        // 2.도서 출력
        public void PrintBookList()
        {
            for(int i=0; i<BookList.Count; i++)
            {
                Console.Write((i+1) + ". ");
                BookList[i].PrintData();
            }
        }

        // 3.도서 검색
        public void SearchBook()
        {
            Console.WriteLine("3.1 ISBN으로 검색");
            Console.WriteLine("3.2 책제목으로 검색");
            Console.WriteLine("3.3 저자로 검색");
            Console.WriteLine("3.4 목차로 검색");

            int iChoice = Util.InputInt("");
            switch (iChoice)
            {
                // ISBN으로 검색
                case 1:
                    SearchByISBN(findBook);
                    break;
                // 책 제목으로 검색
                case 2:
                    SearchBy(findBook, "책 제목: ", Book.ComapareTitle);
                    break;
                // 저자로 검색
                case 3:
                    SearchBy(findBook, "저자: ", Book.CompareAuthor);
                    break;
                // 목차로 검색
                case 4:
                    SearchBy(findBook, "목차: ", Book.CompareContents);
                    break;
                default:
                    Console.WriteLine("선택 항목을 벗어났습니다.");
                    break;
            }
        }

        public void SearchByISBN(FindBook f)
        {
            int isbn = Util.InputInt("ISBN 코드: ");
            int idx = f.Find_ISBN(isbn);
            if(idx != -1) // 검색 결과가 있으면
            {
                BookList[idx].PrintData();
            }
            else // 검색 결과가 없으면
            {
                Console.WriteLine("일치하는 항목이 없습니다.");
            }
        }
        
        public List<int> SearchBy(FindBook f, string text, CompareFuncDele compFunc)
        {
            string s = Util.Input(text);
            List<int> idxList = f.FindWith(s, compFunc);
            if (idxList.Count != 0) // 검색 결과가 0이 아니면
            {
                for (int i = 0; i < idxList.Count; i++)
                {
                    Console.Write((i + 1) + ".");
                    BookList[idxList[i]].PrintData();
                }
            }
            else // 검색 결과 항목이 0이면
            {
                Console.WriteLine("일치하는 항목이 없습니다.");
            }            
            return idxList; // 삭제에서 재사용할 때, 선택된 인덱스를 받기 위함
        }

        // 4.도서 삭제
        public void DeleteBook()
        {
            Console.WriteLine("4.1 책제목으로 검색후 삭제");
            Console.WriteLine("4.2 저자로 검색후 삭제");
            Console.WriteLine("4.3 목차로 검색후 삭제");

            int iChoice = Util.InputInt("");
            switch (iChoice)
            {
                // 책제목으로 검색후 삭제
                case 1:
                    DeleteBy(findBook, "책 제목: ", Book.ComapareTitle);
                    break;
                // 저자로 검색후 삭제
                case 2:
                    DeleteBy(findBook, "저자: ", Book.CompareAuthor);
                    break;
                // 목차로 검색후 삭제
                case 3:
                    DeleteBy(findBook, "목차: ", Book.CompareContents);
                    break;
                default:
                    Console.WriteLine("선택 항목을 벗어났습니다.");
                    break;
            }
        }

        public void DeleteBy(FindBook f, string text, CompareFuncDele compFunc)
        {
            List<int> idxList = SearchBy(f, text, compFunc);
            if (idxList.Count != 0) // 검색 결과가 0이 아니면
            {
                int select_idx = Util.InputInt("선택: ");
                if (select_idx > 0 && select_idx <= idxList.Count) // 선택 범위를 벗어나지 않으면
                {
                    BookList.RemoveAt(idxList[select_idx - 1]);
                }
                else // 선택 범위를 벗어나면
                {
                    Console.WriteLine("선택 범위를 벗어났습니다.");
                }
            }
        }

        // 5.도서 수정
        public void BookUpdate()
        {
            Console.WriteLine("5.1 책제목으로 검색후 수정");
            Console.WriteLine("5.2 저자로 검색후 수정");
            Console.WriteLine("5.3 목차로 검색후 수정");

            int iChoice = Util.InputInt("");
            switch (iChoice)
            {
                // 책제목으로 검색후 삭제
                case 1:
                    UpdateBy(findBook, "책 제목: ", Book.ComapareTitle);
                    break;
                // 저자로 검색후 삭제
                case 2:
                    UpdateBy(findBook, "저자: ", Book.CompareAuthor);
                    break;
                // 목차로 검색후 삭제
                case 3:
                    UpdateBy(findBook, "목차: ", Book.CompareContents);
                    break;
                default:
                    Console.WriteLine("선택 항목을 벗어났습니다.");
                    break;
            }
        }

        public void UpdateBy(FindBook f, string text, CompareFuncDele compFunc)
        {
            List<int> idxList = SearchBy(f, text, compFunc);
            if (idxList.Count != 0) // 검색 결과가 0이 아니면
            {
                int select_idx = Util.InputInt("선택: ");
                if(select_idx > 0 && select_idx <= idxList.Count) // 선택 범위를 벗어나지 않으면
                {
                    BookList[idxList[select_idx - 1]].InputData();
                }
                else // 선택 범위를 벗어나면
                {
                    Console.WriteLine("선택 범위를 벗어났습니다.");
                }
            }         
        }

        public void Menu()
        {
            string choice = "";
            while (choice != "0")
            {
                Console.WriteLine("1.도서등록");
                Console.WriteLine("2.도서출력");
                Console.WriteLine("3.도서검색");
                Console.WriteLine("4.도서삭제");
                Console.WriteLine("5.도서수정");
                choice = Console.ReadLine();
                switch (choice)
                {
                    case "0":
                        break;
                    case "1":
                        CreateBook();
                        break;
                    case "2":
                        PrintBookList();
                        break;
                    case "3":
                        SearchBook();
                        break;
                    case "4":
                        DeleteBook();
                        break;
                    case "5":
                        BookUpdate();
                        break;
                    default:
                        Console.WriteLine("잘못된 입력입니다.");
                        break;
                }
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            BookManager mgr = new BookManager();
            mgr.Menu();
        }
    }
}
