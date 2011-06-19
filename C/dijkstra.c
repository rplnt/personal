#include <stdio.h>
#include <stdlib.h>
#include <limits.h> //INT_MAX


#define MIN(a,b) ((a)<=(b)?(a):(b))

struct vertice;

/* structure for storing graph edges */
struct edge {
  int cost;
  struct vertice* target; //second node on edge, first is the "parent"
  struct edge* next;
};

/* structure for storing graph nodes */
struct vertice {
  int id;
  struct vertice* parent; //path reconstruction
  int visited; //not visited = 0
  int distance;
  struct edge* neighbours;
};

/* structure grouping nodes for easy access */
struct item {
  struct vertice* node;
  struct item* next;
};



/**
  Add new node to list of graph verices
  
  @param head	  head of used list
  @return       newly added node
*/
struct item* addNode(struct item* head) {
  struct item *last, *latest;
  struct vertice* node;
    
  /* find end of the list */
  if ( head != NULL ) {
    last = head;
    while ( last->next != NULL ) {
      last = last->next;
    }
  } else last = NULL;
  
  /* allocate memory */
  latest = malloc(sizeof(struct item));
  if ( latest == NULL ) return last;
  node = malloc(sizeof(struct vertice));
  if ( node == NULL ) {
    free(latest);
    return last;
  }

  node->parent = NULL;
  node->neighbours = NULL;
  node->distance = INT_MAX;  
  node->visited = 0;
  latest->next = NULL;
  latest->node = node;
  
  if ( last == NULL ) {
    node->id = 0;
  } else {
    node->id = last->node->id+1;
    last->next = latest;
  }
  
  return latest; //just in case...
}



/**
  Link nodes A and B; not exactly bulletproof
  
  @param head	  head of used list
  @param cost   cost of given edge
  @param idA	  node A's id
  @param idA	  node B's id
  @return       void
*/
void addEdge(struct item* head, int cost, int idA, int idB) {
  if ( head == NULL ) return; //empty list
  if ( idA == idB ) return;  //can't create self-loops
  
  /* find nodes with ids idA and idB in list */
  struct vertice *pNodeA,*pNodeB;
  struct item *pListItem = head;
  pNodeA = pNodeB = NULL;
  while ( pListItem != NULL ) {
    if ( pNodeA == NULL && pListItem->node->id == idA ) pNodeA = pListItem->node;
    if ( pNodeB == NULL && pListItem->node->id == idB ) pNodeB = pListItem->node;
    if ( pNodeA != NULL && pNodeB != NULL ) break;
    pListItem = pListItem->next;
  }
  if ( pNodeA == NULL || pNodeB == NULL ) return; //link can't be created
  
  /* find places where to put new edge in node A */
  struct edge *pEdgeA = pNodeA->neighbours;
  while ( pEdgeA!=NULL && pEdgeA->next != NULL ) {
    if ( pEdgeA->target == pNodeB ) return; //path exists
    pEdgeA = pEdgeA->next;
  }
  /* find places where to put new edge in node B */
  struct edge *pEdgeB = pNodeB->neighbours;
  while ( pEdgeB!=NULL && pEdgeB->next != NULL ) {
    if ( pEdgeB->target == pNodeA) return; //path exists
    pEdgeB = pEdgeB->next;
  }
  
  /* create edges and link them in */
  struct edge* linkA = malloc(sizeof(struct edge));
  struct edge* linkB = malloc(sizeof(struct edge));
  if ( linkA == NULL || linkB == NULL ) return;
  linkA->next = linkB->next = NULL;
  linkA->cost = linkB->cost = cost;
  linkA->target = pNodeB;
  linkB->target = pNodeA;

  if ( pNodeA->neighbours == NULL ) pNodeA->neighbours = linkA;
    else pEdgeA->next = linkA;
  if ( pNodeB->neighbours == NULL ) pNodeB->neighbours = linkB;
    else pEdgeB->next = linkB; 
    
  return;
}



/**
  Print graph
  
  @param head	  head of used list
  @return       void
*/
void printGraph(struct item* head) {
 
  struct item* pItem = head;
  while ( pItem != NULL ) {
    struct vertice* pNode = pItem->node;
    printf("[%d] ",pNode->id);
    struct edge* link = pNode->neighbours;
    while ( link != NULL ) {
      printf("-> %d|%d (%d) ",pNode->id, link->target->id, link->cost);
      link = link->next;
    }
    printf("\n");
    pItem = pItem->next;
    }
  printf("\n\n");
   
  return;
}



/**
  Dijkstra's algorithm - will fill nodes in given list
  assumes clear graph
  
  @param head	  head of used list
  @param start	id of the node where to start
  @return       void
*/
void dijkstra(struct item* head, int start) {
  if ( head == NULL ) return;
  struct item* pItem;
    
  /* find start */
  pItem = head;
  while ( pItem != NULL ) {
    if ( pItem->node->id == start ) break;
    pItem = pItem->next;
  }
  
  struct vertice* currentNode = pItem->node;
  currentNode->distance = 0;
  while (1) {
    //printf("#%d's final distance: %d\n",currentNode->id,currentNode->distance);
    currentNode->visited = 1;

    /* update neighbours */
    struct edge* link = currentNode->neighbours;
    while ( link != NULL ) {
      if ( link->target->visited == 0 ) {
        int dist = currentNode->distance + link->cost;
        if ( dist < link->target->distance ) {
          link->target->distance = dist;
          link->target->parent = currentNode;
          //printf("  %d's distance updated to: %d\n",link->target->id,dist);
        }
      }
      link = link->next;
    }
    
    /* find next target */
    pItem = head;
    int min = INT_MAX;
    while ( pItem != NULL ) {
      if ( pItem->node->visited == 0 ) {
        min = MIN(min,pItem->node->distance);
        if ( pItem->node->distance == min ) currentNode = pItem->node;
      }
      pItem = pItem->next;
    }
    
    //no new target was found, stop
    if ( min == INT_MAX ) break;
  }
  
  return;
}



/**
  Path reconstruction - will print path
  
  @param head	  head of used list
  @param id   	path from given id to start
  @return       void
*/
void printPath(struct item* head, int id) {
  /* find start */
  struct item* pItem = head;
  while ( pItem != NULL ) {
    if ( pItem->node->id == id ) break;
    pItem = pItem->next;
  }
  if ( pItem == NULL ) return;
  
  struct vertice* pNode = pItem->node;
  printf("Total path price: %d\n%d",pNode->distance,pNode->id);
  while ( pNode->parent != NULL ) {
    pNode = pNode->parent;
    printf(" -> %d",pNode->id);
  }
  printf("\n\n");
  
  return; 
}



void clearGraph(struct item* head); //not implemented :P



int main(void) {
  
  struct item *head, *last;
  head = addNode(NULL); //list has to be initialized this way!
  
  int i; // C99
  for(i=0;i<7;i++) {
    addNode(head);
  }

  addEdge(head,8,0,3);
  addEdge(head,4,0,2);
  addEdge(head,2,1,3);
  addEdge(head,1,2,1);
  addEdge(head,9,2,5);
  addEdge(head,1,3,5);
  addEdge(head,5,3,4);
  addEdge(head,3,5,4);
  addEdge(head,1,5,6);
  addEdge(head,7,5,7);
  addEdge(head,2,4,7);

  //printGraph(head);
  
  dijkstra(head, 0);
  
  for(i=0;i<7;i++) {  
    printPath(head,i);
  }
  
  return 0;
}
