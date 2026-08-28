.class public final La/a/a;
.super La/c/q;


# static fields
.field public static a:Lpmsj/work/a/l;

.field static b:Ljava/lang/StringBuffer;

.field static c:La/c/e;

.field private static u:La/c/q;

.field private static v:La/c/q;

.field private static w:Lpmsj/work/a/l;

.field private static x:La/a/a;


# instance fields
.field private f:La/c/e;

.field private g:I

.field private h:B

.field private i:[I

.field private j:S

.field private k:[B

.field private l:[S

.field private m:[S

.field private n:[S

.field private o:[S

.field private p:[[S

.field private q:[[B

.field private r:[[B

.field private s:[[B

.field private t:[[S


# direct methods
.method static constructor <clinit>()V
    .locals 2

    new-instance v0, La/c/q;

    const v1, 0x927c0

    invoke-direct {v0, v1}, La/c/q;-><init>(I)V

    sput-object v0, La/a/a;->u:La/c/q;

    new-instance v0, Lpmsj/work/a/l;

    invoke-direct {v0}, Lpmsj/work/a/l;-><init>()V

    sput-object v0, La/a/a;->a:Lpmsj/work/a/l;

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    sput-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    new-instance v0, La/c/q;

    const/16 v1, 0x7530

    invoke-direct {v0, v1}, La/c/q;-><init>(I)V

    sput-object v0, La/a/a;->v:La/c/q;

    new-instance v0, Lpmsj/work/a/l;

    invoke-direct {v0}, Lpmsj/work/a/l;-><init>()V

    sput-object v0, La/a/a;->w:Lpmsj/work/a/l;

    new-instance v0, La/c/e;

    invoke-direct {v0}, La/c/e;-><init>()V

    sput-object v0, La/a/a;->c:La/c/e;

    const v0, 0x186a0

    const/4 v1, 0x1

    invoke-static {v0, v1}, La/a/a;->b(IZ)La/a/a;

    move-result-object v0

    sput-object v0, La/a/a;->x:La/a/a;

    return-void
.end method

.method public constructor <init>(I[BZI)V
    .locals 11

    const/4 v1, 0x2

    const/4 v10, 0x0

    invoke-direct {p0, p4}, La/c/q;-><init>(I)V

    iput p1, p0, La/a/a;->g:I

    if-eqz p2, :cond_7

    add-int/lit8 v0, v1, 0x1

    aget-byte v1, p2, v1

    invoke-static {v1}, La/c/x;->a(B)I

    move-result v1

    and-int/lit8 v2, v1, 0x3f

    int-to-byte v2, v2

    iput-byte v2, p0, La/a/a;->h:B

    const/4 v2, 0x3

    add-int/lit8 v0, v0, 0x1

    aget-byte v2, p2, v2

    invoke-static {v2}, La/c/x;->a(B)I

    move-result v2

    shl-int/lit8 v2, v2, 0x2

    shr-int/lit8 v1, v1, 0x6

    or-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, p0, La/a/a;->j:S

    const/4 v1, 0x4

    add-int/lit8 v0, v0, 0x1

    aget-byte v1, p2, v1

    invoke-static {v1}, La/c/x;->a(B)I

    move-result v1

    const/4 v2, 0x5

    add-int/lit8 v0, v0, 0x1

    aget-byte v2, p2, v2

    invoke-static {v2}, La/c/x;->a(B)I

    move-result v2

    add-int/lit8 v0, v0, 0x1

    add-int/lit8 v0, v0, 0x1

    iget-byte v3, p0, La/a/a;->h:B

    new-array v3, v3, [I

    iput-object v3, p0, La/a/a;->i:[I

    move v3, v0

    move v0, v10

    :goto_0
    iget-byte v4, p0, La/a/a;->h:B

    if-ge v0, v4, :cond_0

    iget-object v4, p0, La/a/a;->i:[I

    invoke-static {p2, v3}, La/c/x;->a([BI)I

    move-result v5

    aput v5, v4, v0

    add-int/lit8 v3, v3, 0x4

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    iget-short v0, p0, La/a/a;->j:S

    new-array v0, v0, [B

    iput-object v0, p0, La/a/a;->k:[B

    iget-short v0, p0, La/a/a;->j:S

    new-array v0, v0, [S

    iput-object v0, p0, La/a/a;->l:[S

    iget-short v0, p0, La/a/a;->j:S

    new-array v0, v0, [S

    iput-object v0, p0, La/a/a;->m:[S

    iget-short v0, p0, La/a/a;->j:S

    new-array v0, v0, [S

    iput-object v0, p0, La/a/a;->n:[S

    iget-short v0, p0, La/a/a;->j:S

    new-array v0, v0, [S

    iput-object v0, p0, La/a/a;->o:[S

    move v0, v10

    :goto_1
    iget-short v4, p0, La/a/a;->j:S

    if-ge v0, v4, :cond_1

    iget-object v4, p0, La/a/a;->k:[B

    add-int/lit8 v5, v3, 0x1

    aget-byte v3, p2, v3

    aput-byte v3, v4, v0

    iget-object v3, p0, La/a/a;->l:[S

    add-int/lit8 v4, v5, 0x1

    aget-byte v5, p2, v5

    invoke-static {v5}, La/c/x;->b(B)S

    move-result v5

    aput-short v5, v3, v0

    iget-object v3, p0, La/a/a;->m:[S

    add-int/lit8 v5, v4, 0x1

    aget-byte v4, p2, v4

    invoke-static {v4}, La/c/x;->b(B)S

    move-result v4

    aput-short v4, v3, v0

    iget-object v3, p0, La/a/a;->n:[S

    add-int/lit8 v4, v5, 0x1

    aget-byte v5, p2, v5

    invoke-static {v5}, La/c/x;->b(B)S

    move-result v5

    aput-short v5, v3, v0

    iget-object v3, p0, La/a/a;->o:[S

    add-int/lit8 v5, v4, 0x1

    aget-byte v4, p2, v4

    invoke-static {v4}, La/c/x;->b(B)S

    move-result v4

    aput-short v4, v3, v0

    add-int/lit8 v0, v0, 0x1

    move v3, v5

    goto :goto_1

    :cond_1
    new-array v0, v1, [[S

    iput-object v0, p0, La/a/a;->p:[[S

    new-array v0, v1, [[B

    iput-object v0, p0, La/a/a;->q:[[B

    new-array v0, v1, [[B

    iput-object v0, p0, La/a/a;->r:[[B

    new-array v0, v1, [[B

    iput-object v0, p0, La/a/a;->s:[[B

    move v0, v10

    :goto_2
    if-ge v0, v1, :cond_3

    add-int/lit8 v4, v3, 0x1

    aget-byte v3, p2, v3

    invoke-static {v3}, La/c/x;->a(B)I

    move-result v3

    iget-object v5, p0, La/a/a;->p:[[S

    new-array v6, v3, [S

    aput-object v6, v5, v0

    iget-object v5, p0, La/a/a;->q:[[B

    new-array v6, v3, [B

    aput-object v6, v5, v0

    iget-object v5, p0, La/a/a;->r:[[B

    new-array v6, v3, [B

    aput-object v6, v5, v0

    iget-object v5, p0, La/a/a;->s:[[B

    new-array v6, v3, [B

    aput-object v6, v5, v0

    move v5, v4

    move v4, v10

    :goto_3
    if-ge v4, v3, :cond_2

    add-int/lit8 v6, v5, 0x1

    aget-byte v5, p2, v5

    invoke-static {v5}, La/c/x;->a(B)I

    move-result v5

    add-int/lit8 v7, v6, 0x1

    aget-byte v6, p2, v6

    invoke-static {v6}, La/c/x;->a(B)I

    move-result v6

    iget-object v8, p0, La/a/a;->q:[[B

    aget-object v8, v8, v0

    and-int/lit8 v9, v5, 0x7

    int-to-byte v9, v9

    aput-byte v9, v8, v4

    iget-object v8, p0, La/a/a;->p:[[S

    aget-object v8, v8, v0

    shl-int/lit8 v6, v6, 0x5

    shr-int/lit8 v5, v5, 0x3

    or-int/2addr v5, v6

    int-to-short v5, v5

    aput-short v5, v8, v4

    iget-object v5, p0, La/a/a;->r:[[B

    aget-object v5, v5, v0

    add-int/lit8 v6, v7, 0x1

    aget-byte v7, p2, v7

    aput-byte v7, v5, v4

    iget-object v5, p0, La/a/a;->s:[[B

    aget-object v5, v5, v0

    add-int/lit8 v7, v6, 0x1

    aget-byte v6, p2, v6

    aput-byte v6, v5, v4

    add-int/lit8 v4, v4, 0x1

    move v5, v7

    goto :goto_3

    :cond_2
    add-int/lit8 v0, v0, 0x1

    move v3, v5

    goto :goto_2

    :cond_3
    if-eqz p3, :cond_4

    new-instance v0, La/c/e;

    const/4 v1, 0x6

    invoke-direct {v0, v1}, La/c/e;-><init>(I)V

    iput-object v0, p0, La/a/a;->f:La/c/e;

    :cond_4
    new-array v0, v2, [[S

    iput-object v0, p0, La/a/a;->t:[[S

    move v0, v10

    move v1, v3

    :goto_4
    if-ge v0, v2, :cond_7

    add-int/lit8 v3, v1, 0x1

    aget-byte v1, p2, v1

    invoke-static {v1}, La/c/x;->a(B)I

    move-result v1

    if-eqz p3, :cond_5

    invoke-static {p2, v3}, La/c/x;->a([BI)I

    move-result v4

    iget-object v5, p0, La/a/a;->f:La/c/e;

    new-instance v6, Ljava/lang/Integer;

    invoke-direct {v6, v0}, Ljava/lang/Integer;-><init>(I)V

    invoke-virtual {v5, v4, v6}, La/c/e;->a(ILjava/lang/Object;)Ljava/lang/Object;

    :cond_5
    add-int/lit8 v3, v3, 0x4

    iget-object v4, p0, La/a/a;->t:[[S

    new-array v5, v1, [S

    aput-object v5, v4, v0

    move v4, v3

    move v3, v10

    :goto_5
    if-ge v3, v1, :cond_6

    iget-object v5, p0, La/a/a;->t:[[S

    aget-object v5, v5, v0

    add-int/lit8 v6, v4, 0x1

    aget-byte v4, p2, v4

    invoke-static {v4}, La/c/x;->b(B)S

    move-result v4

    aput-short v4, v5, v3

    add-int/lit8 v4, v6, 0x1

    add-int/lit8 v3, v3, 0x1

    goto :goto_5

    :cond_6
    add-int/lit8 v0, v0, 0x1

    move v1, v4

    goto :goto_4

    :cond_7
    return-void
.end method

.method public static a(IZ)La/a/a;
    .locals 3

    const/4 v2, 0x0

    const v0, 0x186a0

    if-ne v0, p0, :cond_1

    sget-object v0, La/a/a;->x:La/a/a;

    :cond_0
    :goto_0
    return-object v0

    :cond_1
    :try_start_0
    sget-object v0, La/a/a;->a:Lpmsj/work/a/l;

    invoke-virtual {v0, p0}, Lpmsj/work/a/l;->b(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/a/a;

    if-eqz v0, :cond_2

    invoke-virtual {v0}, La/a/a;->a()Z

    move-result v1

    if-eqz v1, :cond_0

    move-object v0, v2

    goto :goto_0

    :cond_2
    sget-object v0, La/a/a;->w:Lpmsj/work/a/l;

    invoke-virtual {v0, p0}, Lpmsj/work/a/l;->b(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/a/a;

    if-nez v0, :cond_0

    invoke-static {p0, p1}, La/a/a;->b(IZ)La/a/a;

    move-result-object v0

    if-eqz v0, :cond_0

    sget-object v1, La/a/a;->w:Lpmsj/work/a/l;

    invoke-virtual {v1, p0, v0}, Lpmsj/work/a/l;->a(ILjava/lang/Object;)Ljava/lang/Object;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v0

    move-object v0, v2

    goto :goto_0
.end method

.method private static b(IZ)La/a/a;
    .locals 4

    const/4 v3, 0x0

    sget-object v0, La/a/a;->c:La/c/e;

    invoke-virtual {v0, p0}, La/c/e;->a(I)Z

    move-result v0

    if-eqz v0, :cond_0

    move-object v0, v3

    :goto_0
    return-object v0

    :cond_0
    sget-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    const/4 v1, 0x0

    sget-object v2, La/a/a;->b:Ljava/lang/StringBuffer;

    invoke-virtual {v2}, Ljava/lang/StringBuffer;->length()I

    move-result v2

    invoke-virtual {v0, v1, v2}, Ljava/lang/StringBuffer;->delete(II)Ljava/lang/StringBuffer;

    sget-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    sget-object v1, Lpmsj/work/a/c;->Y:[Ljava/lang/String;

    const/4 v2, 0x3

    aget-object v1, v1, v2

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    sget-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    invoke-virtual {v0, p0}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    sget-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    const-string v1, ".dat"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    sget-object v0, La/a/a;->b:Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v0}, Lpmsj/work/a/d;->a(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v0

    if-nez v0, :cond_1

    sget-object v0, La/a/a;->c:La/c/e;

    new-instance v1, Ljava/lang/Integer;

    invoke-direct {v1, p0}, Ljava/lang/Integer;-><init>(I)V

    invoke-virtual {v0, p0, v1}, La/c/e;->a(ILjava/lang/Object;)Ljava/lang/Object;

    move-object v0, v3

    goto :goto_0

    :cond_1
    :try_start_0
    invoke-virtual {v0}, Ljava/io/InputStream;->available()I

    move-result v1

    new-array v1, v1, [B
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    :try_start_1
    invoke-virtual {v0, v1}, Ljava/io/InputStream;->read([B)I

    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_1

    move-object v0, v1

    :goto_1
    new-instance v1, La/a/a;

    const/16 v2, 0x7530

    invoke-direct {v1, p0, v0, p1, v2}, La/a/a;-><init>(I[BZI)V

    invoke-static {}, Ljava/lang/System;->gc()V

    move-object v0, v1

    goto :goto_0

    :catch_0
    move-exception v0

    move-object v0, v3

    goto :goto_1

    :catch_1
    move-exception v0

    move-object v0, v1

    goto :goto_1
.end method

.method public static d()V
    .locals 5

    const/4 v4, 0x0

    sget-object v0, La/a/a;->v:La/c/q;

    invoke-virtual {v0}, La/c/q;->f()Z

    move-result v0

    if-eqz v0, :cond_1

    sget-object v0, La/a/a;->w:Lpmsj/work/a/l;

    invoke-virtual {v0}, Lpmsj/work/a/l;->f()I

    move-result v1

    move v2, v4

    :goto_0
    if-ge v2, v1, :cond_1

    sget-object v0, La/a/a;->w:Lpmsj/work/a/l;

    invoke-virtual {v0}, Lpmsj/work/a/l;->g()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/a/a;

    invoke-virtual {v0}, La/a/a;->i()Z

    move-result v3

    if-eqz v3, :cond_0

    sget-object v3, La/a/a;->w:Lpmsj/work/a/l;

    iget v0, v0, La/a/a;->g:I

    invoke-virtual {v3, v0}, Lpmsj/work/a/l;->c(I)Ljava/lang/Object;

    :cond_0
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_0

    :cond_1
    sget-object v0, La/a/a;->u:La/c/q;

    invoke-virtual {v0}, La/c/q;->f()Z

    move-result v0

    if-eqz v0, :cond_3

    sget-object v0, La/a/a;->a:Lpmsj/work/a/l;

    invoke-virtual {v0}, Lpmsj/work/a/l;->f()I

    move-result v1

    move v2, v4

    :goto_1
    if-ge v2, v1, :cond_3

    sget-object v0, La/a/a;->a:Lpmsj/work/a/l;

    invoke-virtual {v0}, Lpmsj/work/a/l;->g()Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/a/a;

    invoke-virtual {v0}, La/a/a;->i()Z

    move-result v3

    if-eqz v3, :cond_2

    sget-object v3, La/a/a;->a:Lpmsj/work/a/l;

    iget v0, v0, La/a/a;->g:I

    invoke-virtual {v3, v0}, Lpmsj/work/a/l;->c(I)Ljava/lang/Object;

    :cond_2
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_1

    :cond_3
    return-void
.end method


# virtual methods
.method public final a(I)I
    .locals 1

    iget-object v0, p0, La/a/a;->i:[I

    aget v0, v0, p1

    return v0
.end method

.method public final a(IILjavax/microedition/lcdui/Graphics;IILjava/util/Vector;B)V
    .locals 19

    invoke-virtual/range {p0 .. p0}, La/a/a;->e()V

    if-ltz p4, :cond_0

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->t:[[S

    move-object v3, v0

    array-length v3, v3

    move/from16 v0, p4

    move v1, v3

    if-lt v0, v1, :cond_1

    :cond_0
    return-void

    :cond_1
    if-ltz p5, :cond_0

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->t:[[S

    move-object v3, v0

    aget-object v3, v3, p4

    array-length v3, v3

    move/from16 v0, p5

    move v1, v3

    if-ge v0, v1, :cond_0

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->t:[[S

    move-object v3, v0

    aget-object v3, v3, p4

    aget-short v3, v3, p5

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->p:[[S

    move-object v4, v0

    aget-object v12, v4, v3

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->q:[[B

    move-object v4, v0

    aget-object v13, v4, v3

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->r:[[B

    move-object v4, v0

    aget-object v14, v4, v3

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->s:[[B

    move-object v4, v0

    aget-object v15, v4, v3

    move-object v0, v12

    array-length v0, v0

    move/from16 v16, v0

    const/4 v3, 0x0

    move/from16 v17, v3

    :goto_0
    move/from16 v0, v17

    move/from16 v1, v16

    if-ge v0, v1, :cond_0

    aget-short v4, v12, v17

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->k:[B

    move-object v3, v0

    aget-byte v18, v3, v4

    invoke-virtual/range {p6 .. p6}, Ljava/util/Vector;->size()I

    move-result v3

    move/from16 v0, v18

    move v1, v3

    if-ge v0, v1, :cond_4

    move-object/from16 v0, p6

    move/from16 v1, v18

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    if-eqz v3, :cond_4

    move-object/from16 v0, p6

    move/from16 v1, v18

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p4

    check-cast p4, Ljava/lang/Integer;

    invoke-virtual/range {p4 .. p4}, Ljava/lang/Integer;->intValue()I

    move-result v3

    move v5, v3

    :goto_1
    if-eqz v5, :cond_3

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->n:[S

    move-object v3, v0

    aget-short v7, v3, v4

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->o:[S

    move-object v3, v0

    aget-short v8, v3, v4

    aget-byte v3, v13, v17

    aget-byte v6, v14, v17

    aget-byte v11, v15, v17

    const/4 v9, 0x2

    move v0, v9

    move/from16 v1, p7

    if-ne v0, v1, :cond_2

    packed-switch v3, :pswitch_data_0

    :cond_2
    move v9, v3

    move v10, v6

    :goto_2
    :try_start_0
    invoke-static {v5}, La/a/f;->a(I)La/a/e;

    move-result-object v3

    if-eqz v3, :cond_5

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->l:[S

    move-object v5, v0

    aget-short v5, v5, v4

    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->m:[S

    move-object v6, v0

    aget-short v6, v6, v4

    add-int v10, v10, p1

    add-int v11, v11, p2

    move-object/from16 v4, p3

    invoke-virtual/range {v3 .. v11}, La/a/e;->a(Ljavax/microedition/lcdui/Graphics;IIIIIII)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :cond_3
    :goto_3
    add-int/lit8 v3, v17, 0x1

    move/from16 v17, v3

    goto :goto_0

    :cond_4
    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->i:[I

    move-object v3, v0

    aget v3, v3, v18

    move v5, v3

    goto :goto_1

    :pswitch_0
    neg-int v3, v6

    sub-int/2addr v3, v7

    const/4 v6, 0x2

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_1
    neg-int v3, v6

    sub-int/2addr v3, v7

    const/4 v6, 0x0

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_2
    neg-int v3, v6

    sub-int/2addr v3, v7

    const/4 v6, 0x3

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_3
    neg-int v3, v6

    sub-int/2addr v3, v7

    const/4 v6, 0x1

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_4
    neg-int v3, v6

    sub-int/2addr v3, v8

    const/4 v6, 0x4

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_5
    neg-int v3, v6

    sub-int/2addr v3, v8

    const/4 v6, 0x5

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_6
    neg-int v3, v6

    sub-int/2addr v3, v8

    const/4 v6, 0x7

    move v9, v6

    move v10, v3

    goto :goto_2

    :pswitch_7
    neg-int v3, v6

    sub-int/2addr v3, v8

    const/4 v6, 0x6

    move v9, v6

    move v10, v3

    goto :goto_2

    :cond_5
    :try_start_1
    sget-object v3, La/a/f;->i:La/a/c;

    invoke-virtual {v3, v5}, La/a/c;->c(I)Z

    move-result v3

    if-eqz v3, :cond_3

    const/4 v3, 0x1

    new-array v3, v3, [I

    const/4 v4, 0x0

    aput v5, v3, v4

    const/16 v4, 0x5de

    const/4 v5, 0x2

    invoke-static {v4, v5, v3}, Lpmsj/work/main/w;->a(IB[I)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    goto :goto_3

    :catch_0
    move-exception v3

    invoke-virtual/range {p6 .. p6}, Ljava/util/Vector;->size()I

    move-result v3

    move/from16 v0, v18

    move v1, v3

    if-ge v0, v1, :cond_6

    move-object/from16 v0, p6

    move/from16 v1, v18

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    if-eqz v3, :cond_6

    new-instance v3, Ljava/lang/Integer;

    const/4 v4, 0x0

    invoke-direct {v3, v4}, Ljava/lang/Integer;-><init>(I)V

    move-object/from16 v0, p6

    move-object v1, v3

    move/from16 v2, v18

    invoke-virtual {v0, v1, v2}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    goto :goto_3

    :cond_6
    move-object/from16 v0, p0

    iget-object v0, v0, La/a/a;->i:[I

    move-object v3, v0

    const/4 v4, 0x0

    aput v4, v3, v18

    goto :goto_3

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_2
        :pswitch_1
        :pswitch_3
        :pswitch_5
        :pswitch_4
        :pswitch_6
        :pswitch_7
    .end packed-switch
.end method

.method public final a()Z
    .locals 1

    iget-object v0, p0, La/a/a;->t:[[S

    if-nez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method public final b()I
    .locals 1

    iget v0, p0, La/a/a;->g:I

    return v0
.end method

.method public final b(I)I
    .locals 1

    iget-object v0, p0, La/a/a;->t:[[S

    array-length v0, v0

    if-lt p1, v0, :cond_0

    const/4 v0, 0x0

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, La/a/a;->t:[[S

    aget-object v0, v0, p1

    array-length v0, v0

    goto :goto_0
.end method

.method public final c()I
    .locals 1

    iget-byte v0, p0, La/a/a;->h:B

    return v0
.end method

.method public final c(I)I
    .locals 2

    const/4 v1, -0x1

    iget-object v0, p0, La/a/a;->f:La/c/e;

    if-nez v0, :cond_0

    move v0, v1

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, La/a/a;->f:La/c/e;

    invoke-virtual {v0, p1}, La/c/e;->b(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Ljava/lang/Integer;

    if-nez p0, :cond_1

    move v0, v1

    goto :goto_0

    :cond_1
    invoke-virtual {p0}, Ljava/lang/Integer;->intValue()I

    move-result v0

    goto :goto_0
.end method

.method public final d(I)I
    .locals 5

    const/4 v4, 0x0

    iget-object v0, p0, La/a/a;->t:[[S

    if-nez v0, :cond_0

    move v0, v4

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, La/a/a;->t:[[S

    array-length v0, v0

    if-lt p1, v0, :cond_1

    move v0, v4

    goto :goto_0

    :cond_1
    iget-object v0, p0, La/a/a;->t:[[S

    aget-object v0, v0, p1

    array-length v0, v0

    if-nez v0, :cond_2

    move v0, v4

    goto :goto_0

    :cond_2
    iget-object v0, p0, La/a/a;->t:[[S

    aget-object v0, v0, p1

    aget-short v0, v0, v4

    iget-object v1, p0, La/a/a;->s:[[B

    aget-object v0, v1, v0

    array-length v1, v0

    const/4 v2, 0x1

    sub-int/2addr v1, v2

    move v2, v4

    :goto_1
    if-ltz v1, :cond_4

    aget-byte v3, v0, v1

    if-ge v3, v2, :cond_3

    aget-byte v2, v0, v1

    :cond_3
    add-int/lit8 v1, v1, -0x1

    goto :goto_1

    :cond_4
    neg-int v0, v2

    invoke-static {v0, v4}, Ljava/lang/Math;->max(II)I

    move-result v0

    goto :goto_0
.end method
