program ReverseSinglyLinkedList;

uses
	singlyUtil;

//type
//  ListNode = ^Node;
//  Node = record
//    data: String;
//    next: ListNode;
//  end;

procedure reverseSinglyLinkedList(var head: ListNode);
var
  prev, curr, nxt: ListNode;
begin
  prev := nil;
  curr := head;
  
  while curr <> nil do
    begin
      nxt := curr^.next;
      curr^.next := prev;
      prev := curr;
      curr := nxt
    end;
  
  head := prev;
end;



var
  myList: ListNode;
begin
  myList := convertLineToLL('');

  reverseSinglyLinkedList(myList);

  printLinkedList(myList);

  freeLinkedList(myList);
end.
