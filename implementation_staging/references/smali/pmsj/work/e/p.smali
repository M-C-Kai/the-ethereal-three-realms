.class public final Lpmsj/work/e/p;
.super Lpmsj/work/d/c;


# instance fields
.field private final K:B

.field private final L:B

.field private final M:B

.field private final N:B

.field private final O:B

.field private final P:B

.field private final Q:B

.field private R:B

.field private S:I

.field private T:I

.field private final U:B

.field private final a:I

.field private final b:I

.field private c:Lpmsj/work/d/l;

.field private d:Ljava/util/Vector;

.field private e:Lpmsj/work/d/i;

.field private final f:B


# direct methods
.method public constructor <init>()V
    .locals 2

    const/4 v1, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const v0, 0x497ca

    iput v0, p0, Lpmsj/work/e/p;->a:I

    const v0, 0x497cb

    iput v0, p0, Lpmsj/work/e/p;->b:I

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    iput-byte v1, p0, Lpmsj/work/e/p;->f:B

    const/4 v0, 0x1

    iput-byte v0, p0, Lpmsj/work/e/p;->K:B

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/e/p;->L:B

    const/4 v0, 0x3

    iput-byte v0, p0, Lpmsj/work/e/p;->M:B

    const/4 v0, 0x4

    iput-byte v0, p0, Lpmsj/work/e/p;->N:B

    const/4 v0, 0x5

    iput-byte v0, p0, Lpmsj/work/e/p;->O:B

    const/4 v0, 0x6

    iput-byte v0, p0, Lpmsj/work/e/p;->P:B

    const/4 v0, 0x7

    iput-byte v0, p0, Lpmsj/work/e/p;->Q:B

    const/16 v0, 0x17

    iput-byte v0, p0, Lpmsj/work/e/p;->R:B

    iput-byte v1, p0, Lpmsj/work/e/p;->U:B

    return-void
.end method

.method private static a(La/c/a;)Ljava/lang/String;
    .locals 7

    const/4 v6, 0x5

    const/4 v5, 0x1

    const/4 v4, 0x0

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, La/c/a;->a(I)I

    move-result v0

    invoke-virtual {p0, v4}, La/c/a;->a(I)I

    move-result v1

    if-ne v5, v1, :cond_2

    invoke-static {v0}, Lpmsj/work/b/j;->j(I)I

    move-result v1

    :goto_0
    new-instance v2, Ljava/lang/StringBuffer;

    const/4 v3, 0x6

    invoke-virtual {p0, v3}, La/c/a;->a(I)I

    move-result v3

    invoke-static {v4, v3, v1, v4}, Lpmsj/work/a/k;->a(IIII)Ljava/lang/String;

    move-result-object v1

    invoke-direct {v2, v1}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const/16 v1, 0x20

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-static {v0}, Lpmsj/work/b/j;->g(I)Z

    move-result v1

    if-eqz v1, :cond_1

    invoke-virtual {p0, v6}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-static {v0}, Lpmsj/work/b/j;->j(I)I

    move-result v0

    sget-object v3, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    array-length v3, v3

    sub-int/2addr v3, v5

    invoke-static {v3, v0}, Ljava/lang/Math;->min(II)I

    move-result v0

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    sget-object v4, Lpmsj/work/a/c;->at:[Ljava/lang/String;

    aget-object v0, v4, v0

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_1
    const/4 v0, 0x3

    invoke-virtual {p0, v0}, La/c/a;->a(I)I

    move-result v0

    if-le v0, v5, :cond_0

    const/16 v1, 0xd7

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    :cond_0
    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0

    :cond_1
    invoke-virtual {p0, v6}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_1

    :cond_2
    move v1, v4

    goto :goto_0
.end method

.method private b(La/c/a;)V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-static {p1}, Lpmsj/work/e/p;->a(La/c/a;)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const/4 v1, 0x4

    invoke-virtual {p1, v1}, La/c/a;->a(I)I

    move-result v1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->j()I

    move-result v2

    if-le v1, v2, :cond_0

    const-string v2, "*2"

    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_0
    invoke-static {v1}, La/c/x;->g(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    return-void

    :cond_0
    const-string v2, "*0"

    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_0
.end method

.method private j()V
    .locals 1

    const v0, 0x497cb

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->w(I)Lpmsj/work/d/b;

    move-result-object p0

    check-cast p0, Lpmsj/work/d/l;

    invoke-virtual {p0}, Lpmsj/work/d/l;->k()V

    const-string v0, "\u540d\u79f0"

    invoke-virtual {p0, v0}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    const-string v0, "\u4ef7\u683c"

    invoke-virtual {p0, v0}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    return-void
.end method

.method private k()Z
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    iget-object v1, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/i;->d(I)Z

    move-result v0

    return v0
.end method

.method private n()La/c/a;
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->h()I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    if-lt v0, v1, :cond_0

    const/4 v0, 0x0

    :goto_0
    return-object v0

    :cond_0
    iget-object v1, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/a;

    move-object v0, p0

    goto :goto_0
.end method


# virtual methods
.method public final a(BII)V
    .locals 0

    iput-byte p1, p0, Lpmsj/work/e/p;->R:B

    iput p2, p0, Lpmsj/work/e/p;->S:I

    iput p3, p0, Lpmsj/work/e/p;->T:I

    return-void
.end method

.method public final a(Lpmsj/work/main/w;)V
    .locals 9

    const/4 v8, 0x0

    const/4 v7, 0x1

    invoke-virtual {p1, v8}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    const/4 v0, 0x3

    invoke-virtual {p1, v0}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    move v2, v8

    :goto_1
    if-ge v2, v1, :cond_4

    const/16 v0, 0x8

    mul-int/lit8 v3, v2, 0x8

    add-int/lit8 v3, v3, 0x4

    invoke-virtual {p1, v0, v3}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v3

    invoke-virtual {v3, v7}, La/c/a;->a(I)I

    move-result v4

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v5

    move v6, v8

    :goto_2
    if-ge v6, v5, :cond_3

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v7}, La/c/a;->a(I)I

    move-result v0

    if-ne v4, v0, :cond_2

    move v0, v7

    :goto_3
    if-nez v0, :cond_1

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-direct {p0, v3}, Lpmsj/work/e/p;->b(La/c/a;)V

    :cond_1
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_1

    :cond_2
    add-int/lit8 v0, v6, 0x1

    move v6, v0

    goto :goto_2

    :cond_3
    move v0, v8

    goto :goto_3

    :cond_4
    iget-object v0, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {p1, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/i;->a(I)V

    invoke-direct {p0}, Lpmsj/work/e/p;->j()V

    goto :goto_0

    :sswitch_1
    invoke-virtual {p1, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v8

    :goto_4
    if-ge v3, v2, :cond_0

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v7}, La/c/a;->a(I)I

    move-result v0

    if-ne v1, v0, :cond_6

    iget-object v0, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {v0}, Lpmsj/work/d/i;->a()I

    move-result v1

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->removeElementAt(I)V

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->j()V

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v8

    :goto_5
    if-ge v3, v2, :cond_5

    iget-object v0, p0, Lpmsj/work/e/p;->d:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-direct {p0, v0}, Lpmsj/work/e/p;->b(La/c/a;)V

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_5

    :cond_5
    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->i()V

    iget-object v0, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    sub-int/2addr v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/d/i;->a(I)V

    invoke-direct {p0}, Lpmsj/work/e/p;->j()V

    invoke-direct {p0}, Lpmsj/work/e/p;->k()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/p;->i()V

    goto/16 :goto_0

    :cond_6
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_4

    nop

    :sswitch_data_0
    .sparse-switch
        0x1 -> :sswitch_0
        0xc -> :sswitch_1
        0x10 -> :sswitch_1
    .end sparse-switch
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 7

    const/4 v6, 0x7

    const/4 v5, 0x0

    const/4 v4, 0x1

    invoke-direct {p0}, Lpmsj/work/e/p;->n()La/c/a;

    move-result-object v0

    if-nez v0, :cond_0

    move v0, v4

    :goto_0
    return v0

    :cond_0
    const-string v1, "\u8d2d\u4e70\u7269\u54c1"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_1

    const-string v1, "\u8d2d\u4e70\u5ba0\u7269"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_6

    :cond_1
    const/4 v1, 0x4

    invoke-virtual {v0, v1}, La/c/a;->a(I)I

    move-result v1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->j()I

    move-result v2

    if-le v1, v2, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u94f6\u4e24\u4e0d\u8db3"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    :cond_2
    :goto_1
    move v0, v4

    goto :goto_0

    :cond_3
    invoke-virtual {v0, v5}, La/c/a;->a(I)I

    move-result v2

    if-ne v4, v2, :cond_4

    invoke-static {}, Lpmsj/work/b/a;->c()I

    move-result v2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/ab;->g()I

    move-result v3

    if-lt v2, v3, :cond_4

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u80cc\u5305\u5df2\u6ee1"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_1

    :cond_4
    const/4 v2, 0x3

    invoke-virtual {v0, v5}, La/c/a;->a(I)I

    move-result v3

    if-ne v2, v3, :cond_5

    invoke-static {}, Lpmsj/work/b/f;->a()I

    move-result v2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/ab;->m()I

    move-result v3

    if-lt v2, v3, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u5ba0\u7269\u80cc\u5305\u5df2\u6ee1"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_1

    :cond_5
    new-instance v2, Ljava/lang/StringBuffer;

    const-string v3, "\u786e\u5b9a\u82b1"

    invoke-direct {v2, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, "*3"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "*0"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\u94f6\u4e24"

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v2, p1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v1, 0x5f

    invoke-virtual {v2, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-static {v0}, Lpmsj/work/e/p;->a(La/c/a;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v2, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1, v5, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto :goto_1

    :cond_6
    const-string v1, "\u67e5\u770b\u7269\u54c1"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_7

    const/16 v1, 0x408

    const/16 v2, 0x9

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v0

    invoke-static {v1, v2, v0}, Lpmsj/work/main/w;->a(IBI)V

    goto/16 :goto_1

    :cond_7
    const-string v1, "\u67e5\u770b\u5ba0\u7269"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_8

    const/16 v1, 0x467

    const/4 v2, 0x6

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v3

    invoke-static {v1, v2, v3}, Lpmsj/work/main/w;->a(IBI)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/d/n;->i(I)Lpmsj/work/e/ei;

    goto/16 :goto_1

    :cond_8
    const-string v1, "\u67e5\u770b\u5bf9\u65b9"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_9

    const/16 v1, 0x517

    new-instance v2, La/c/h;

    const/4 v3, 0x2

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    invoke-direct {v3, v5}, La/c/m;-><init>(I)V

    iget-object v0, v0, La/c/a;->a:[La/c/i;

    aget-object v0, v0, v6

    invoke-static {v1, v2, v3, v0}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;)V

    goto/16 :goto_1

    :cond_9
    const-string v1, "\u52a0\u4e3a\u597d\u53cb"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_a

    invoke-virtual {v0, v6}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-static {v5, v0}, Lpmsj/work/main/i;->a(ILjava/lang/String;)V

    goto/16 :goto_1

    :cond_a
    const-string v1, "\u8054\u7cfb\u5356\u5bb6"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x15

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/w;

    invoke-virtual {v0, v6}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/w;->g(Ljava/lang/String;)V

    goto/16 :goto_1
.end method

.method protected final c()V
    .locals 2

    const v0, 0x497ca

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    const/4 v1, 0x3

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->l(I)V

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->g()Lpmsj/work/d/i;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    const-string v0, "\u5bc4\u552e\u8d2d\u4e70"

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->d(Ljava/lang/String;)V

    return-void
.end method

.method protected final c(Lpmsj/work/d/b;)V
    .locals 7

    const/4 v3, 0x5

    const/4 v6, 0x3

    const/4 v5, 0x1

    const/4 v4, 0x0

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    if-ne v0, p1, :cond_3

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0, v3}, Ljava/util/Vector;-><init>(I)V

    invoke-direct {p0}, Lpmsj/work/e/p;->n()La/c/a;

    move-result-object v1

    invoke-virtual {v1, v4}, La/c/a;->a(I)I

    move-result v2

    if-ne v5, v2, :cond_4

    const-string v2, "\u67e5\u770b\u7269\u54c1"

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_0
    :goto_0
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->p()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v3}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_1

    invoke-virtual {v1, v4}, La/c/a;->a(I)I

    move-result v2

    if-ne v5, v2, :cond_5

    const-string v2, "\u8d2d\u4e70\u7269\u54c1"

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_1
    :goto_1
    if-eqz v1, :cond_2

    const/4 v2, 0x7

    invoke-virtual {v1, v2}, La/c/a;->b(I)Ljava/lang/String;

    move-result-object v1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->p()Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_2

    const-string v1, "\u67e5\u770b\u5bf9\u65b9"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u52a0\u4e3a\u597d\u53cb"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u8054\u7cfb\u5356\u5bb6"

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v0, p0}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;)V

    :cond_3
    return-void

    :cond_4
    invoke-virtual {v1, v4}, La/c/a;->a(I)I

    move-result v2

    if-ne v6, v2, :cond_0

    const-string v2, "\u67e5\u770b\u5ba0\u7269"

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_0

    :cond_5
    invoke-virtual {v1, v4}, La/c/a;->a(I)I

    move-result v2

    if-ne v6, v2, :cond_1

    const-string v2, "\u8d2d\u4e70\u5ba0\u7269"

    invoke-virtual {v0, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1
.end method

.method public final c_(I)V
    .locals 4

    if-nez p1, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/p;->n()La/c/a;

    move-result-object v0

    if-eqz v0, :cond_0

    const/16 v1, 0x472

    const/4 v2, 0x4

    const/4 v3, 0x1

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/m;->h()I

    move-result v3

    invoke-static {v1, v2, v0, v3}, Lpmsj/work/main/w;->a(IBII)V

    :cond_0
    return-void
.end method

.method protected final e(Lpmsj/work/d/b;)V
    .locals 1

    iget-object v0, p0, Lpmsj/work/e/p;->c:Lpmsj/work/d/l;

    if-ne v0, p1, :cond_0

    invoke-direct {p0}, Lpmsj/work/e/p;->k()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/p;->i()V

    :cond_0
    return-void
.end method

.method public final i()V
    .locals 10

    const/16 v0, 0x472

    const/16 v2, 0x17

    const/4 v9, 0x0

    const/4 v8, 0x1

    iget v1, p0, Lpmsj/work/e/p;->S:I

    if-eqz v1, :cond_0

    new-instance v1, La/c/h;

    iget-byte v2, p0, Lpmsj/work/e/p;->R:B

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/o;

    iget-object v3, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {v3}, Lpmsj/work/d/i;->c()I

    move-result v3

    int-to-short v3, v3

    invoke-direct {v2, v3}, La/c/o;-><init>(S)V

    new-instance v3, La/c/h;

    iget-object v4, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {v4}, Lpmsj/work/d/i;->d()I

    move-result v4

    int-to-byte v4, v4

    invoke-direct {v3, v4}, La/c/h;-><init>(B)V

    new-instance v4, La/c/m;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/m;->h()I

    move-result v5

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    iget v6, p0, Lpmsj/work/e/p;->S:I

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    iget v7, p0, Lpmsj/work/e/p;->T:I

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v6}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    :goto_0
    invoke-static {v8, v9}, Lpmsj/work/main/t;->a(ZZ)V

    return-void

    :cond_0
    iget-byte v1, p0, Lpmsj/work/e/p;->R:B

    if-ne v1, v2, :cond_1

    :goto_1
    new-instance v1, La/c/h;

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/m;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/m;->h()I

    move-result v3

    invoke-direct {v2, v3}, La/c/m;-><init>(I)V

    new-instance v3, La/c/m;

    invoke-virtual {p0}, Lpmsj/work/e/p;->af()I

    move-result v4

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/o;

    iget-object v5, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {v5}, Lpmsj/work/d/i;->c()I

    move-result v5

    int-to-short v5, v5

    invoke-direct {v4, v5}, La/c/o;-><init>(S)V

    new-instance v5, La/c/h;

    iget-object v6, p0, Lpmsj/work/e/p;->e:Lpmsj/work/d/i;

    invoke-virtual {v6}, Lpmsj/work/d/i;->d()I

    move-result v6

    int-to-byte v6, v6

    invoke-direct {v5, v6}, La/c/h;-><init>(B)V

    invoke-static/range {v0 .. v5}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto :goto_0

    :cond_1
    iget-byte v1, p0, Lpmsj/work/e/p;->R:B

    if-ne v1, v8, :cond_2

    move v2, v8

    goto :goto_1

    :cond_2
    move v2, v9

    goto :goto_1
.end method

.method public final y(I)V
    .locals 0

    invoke-super {p0, p1}, Lpmsj/work/d/c;->y(I)V

    invoke-virtual {p0}, Lpmsj/work/e/p;->i()V

    return-void
.end method
