.class public final Lpmsj/work/e/s;
.super Lpmsj/work/d/c;


# instance fields
.field private final K:B

.field private final L:B

.field private final M:B

.field private final N:B

.field private final O:B

.field private final P:B

.field private final Q:B

.field private final R:B

.field private final S:B

.field private final T:B

.field private final U:B

.field private final V:B

.field private final W:B

.field private final X:B

.field private final Y:B

.field private Z:Lpmsj/work/d/g;

.field private final a:I

.field private aa:[I

.field private ab:[Ljava/lang/String;

.field private ac:[B

.field private final ad:B

.field private final b:I

.field private final c:I

.field private final d:B

.field private final e:B

.field private final f:B


# direct methods
.method public constructor <init>()V
    .locals 3

    const/4 v2, 0x1

    const/4 v1, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const v0, 0x11559

    iput v0, p0, Lpmsj/work/e/s;->a:I

    const v0, 0x1155a

    iput v0, p0, Lpmsj/work/e/s;->b:I

    const v0, 0x1155e

    iput v0, p0, Lpmsj/work/e/s;->c:I

    iput-byte v1, p0, Lpmsj/work/e/s;->d:B

    iput-byte v1, p0, Lpmsj/work/e/s;->e:B

    iput-byte v2, p0, Lpmsj/work/e/s;->f:B

    const/4 v0, 0x2

    iput-byte v0, p0, Lpmsj/work/e/s;->K:B

    const/4 v0, 0x3

    iput-byte v0, p0, Lpmsj/work/e/s;->L:B

    const/4 v0, 0x4

    iput-byte v0, p0, Lpmsj/work/e/s;->M:B

    const/4 v0, 0x5

    iput-byte v0, p0, Lpmsj/work/e/s;->N:B

    const/4 v0, 0x6

    iput-byte v0, p0, Lpmsj/work/e/s;->O:B

    const/4 v0, 0x7

    iput-byte v0, p0, Lpmsj/work/e/s;->P:B

    const/16 v0, 0x8

    iput-byte v0, p0, Lpmsj/work/e/s;->Q:B

    const/16 v0, 0x9

    iput-byte v0, p0, Lpmsj/work/e/s;->R:B

    const/16 v0, 0xa

    iput-byte v0, p0, Lpmsj/work/e/s;->S:B

    const/16 v0, 0xb

    iput-byte v0, p0, Lpmsj/work/e/s;->T:B

    const/16 v0, 0x10

    iput-byte v0, p0, Lpmsj/work/e/s;->U:B

    const/16 v0, 0x11

    iput-byte v0, p0, Lpmsj/work/e/s;->V:B

    const/16 v0, 0x1e

    iput-byte v0, p0, Lpmsj/work/e/s;->W:B

    const/16 v0, 0x61

    iput-byte v0, p0, Lpmsj/work/e/s;->X:B

    const/16 v0, 0x62

    iput-byte v0, p0, Lpmsj/work/e/s;->Y:B

    iput-byte v2, p0, Lpmsj/work/e/s;->ad:B

    return-void
.end method

.method private static C(I)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x49

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/p;

    const/16 v1, 0x17

    invoke-virtual {v0, v1, v2, v2}, Lpmsj/work/e/p;->a(BII)V

    invoke-virtual {v0, p0}, Lpmsj/work/e/p;->y(I)V

    return-void
.end method

.method private static D(I)V
    .locals 4

    const/4 v3, 0x0

    mul-int/lit8 v0, p0, 0xa

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x49

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/p;

    const/4 v1, 0x1

    invoke-virtual {p0, v1, v3, v3}, Lpmsj/work/e/p;->a(BII)V

    invoke-virtual {p0, v0}, Lpmsj/work/e/p;->y(I)V

    return-void
.end method


# virtual methods
.method public final a(Lpmsj/work/main/w;)V
    .locals 6

    const/16 v5, 0x9

    const/4 v2, 0x0

    invoke-virtual {p0}, Lpmsj/work/e/s;->af()I

    move-result v0

    const/16 v1, 0xafa

    if-ne v0, v1, :cond_0

    const v0, 0x1155e

    invoke-virtual {p0, v0}, Lpmsj/work/e/s;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    const-string v1, "\u9009\u62e9\u5ba0\u7269\u7c7b\u578b\uff1a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/b;->a_(Ljava/lang/String;)V

    :cond_0
    const/4 v0, 0x1

    invoke-virtual {p1, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-gtz v0, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u5f53\u524d\u65e0\u6b64\u79cd\u7c7b\u578b\u7269\u54c1\u5bc4\u552e"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    :cond_1
    :goto_0
    return-void

    :cond_2
    new-array v1, v0, [I

    iput-object v1, p0, Lpmsj/work/e/s;->aa:[I

    new-array v1, v0, [Ljava/lang/String;

    iput-object v1, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    new-array v1, v0, [B

    iput-object v1, p0, Lpmsj/work/e/s;->ac:[B

    iget-object v1, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    invoke-virtual {v1, v0}, Lpmsj/work/d/g;->c(I)V

    invoke-virtual {p1, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    sparse-switch v1, :sswitch_data_0

    goto :goto_0

    :sswitch_0
    move v1, v2

    :goto_1
    if-ge v1, v0, :cond_1

    iget-object v2, p0, Lpmsj/work/e/s;->aa:[I

    mul-int/lit8 v3, v1, 0x3

    add-int/lit8 v3, v3, 0x2

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    aput v3, v2, v1

    iget-object v2, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    mul-int/lit8 v3, v1, 0x3

    add-int/lit8 v3, v3, 0x3

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v2, v1

    iget-object v2, p0, Lpmsj/work/e/s;->ac:[B

    mul-int/lit8 v3, v1, 0x3

    add-int/lit8 v3, v3, 0x4

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    aput-byte v3, v2, v1

    new-instance v2, Lpmsj/work/d/a;

    iget-object v3, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    aget-object v3, v3, v1

    sget-object v4, Lpmsj/work/a/c;->v:[I

    aget v4, v4, v5

    invoke-direct {v2, v3, v4}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;I)V

    iget-object v3, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    invoke-virtual {v3, v2, v1}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    :sswitch_1
    move v1, v2

    :goto_2
    if-ge v1, v0, :cond_1

    iget-object v2, p0, Lpmsj/work/e/s;->aa:[I

    mul-int/lit8 v3, v1, 0x2

    add-int/lit8 v3, v3, 0x2

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    aput v3, v2, v1

    iget-object v2, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    mul-int/lit8 v3, v1, 0x2

    add-int/lit8 v3, v3, 0x3

    invoke-virtual {p1, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    aput-object v3, v2, v1

    new-instance v2, Lpmsj/work/d/a;

    iget-object v3, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    aget-object v3, v3, v1

    sget-object v4, Lpmsj/work/a/c;->v:[I

    aget v4, v4, v5

    invoke-direct {v2, v3, v4}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;I)V

    iget-object v3, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    invoke-virtual {v3, v2, v1}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_2

    nop

    :sswitch_data_0
    .sparse-switch
        0x3 -> :sswitch_0
        0x16 -> :sswitch_1
    .end sparse-switch
.end method

.method protected final b(Lpmsj/work/d/b;)V
    .locals 5

    const/16 v4, 0xafa

    const/16 v3, 0xaf9

    const/4 v2, 0x0

    iget v0, p1, Lpmsj/work/d/b;->g:I

    const v1, 0x11559

    if-ne v0, v1, :cond_2

    iget v0, p0, Lpmsj/work/e/s;->I:I

    if-ne v3, v0, :cond_1

    invoke-static {v2}, Lpmsj/work/e/s;->D(I)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    iget v0, p0, Lpmsj/work/e/s;->I:I

    if-ne v4, v0, :cond_0

    invoke-static {v2}, Lpmsj/work/e/s;->C(I)V

    goto :goto_0

    :cond_2
    iget v0, p1, Lpmsj/work/d/b;->g:I

    const v1, 0x1155a

    if-ne v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    invoke-virtual {v0}, Lpmsj/work/d/g;->f()I

    move-result v0

    iget-object v1, p0, Lpmsj/work/e/s;->aa:[I

    array-length v1, v1

    if-ge v0, v1, :cond_0

    iget v1, p0, Lpmsj/work/e/s;->I:I

    if-ne v3, v1, :cond_4

    iget-object v1, p0, Lpmsj/work/e/s;->ac:[B

    aget-byte v1, v1, v0

    const/4 v2, 0x1

    if-ne v1, v2, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x2c

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v1

    iget-object v2, p0, Lpmsj/work/e/s;->ab:[Ljava/lang/String;

    aget-object v2, v2, v0

    invoke-virtual {v1, v2}, Lpmsj/work/d/c;->d(Ljava/lang/String;)V

    const/16 v1, 0x472

    const/16 v2, 0xd

    iget-object v3, p0, Lpmsj/work/e/s;->aa:[I

    aget v0, v3, v0

    int-to-byte v0, v0

    invoke-static {v1, v2, v0}, Lpmsj/work/main/w;->a(IBB)V

    goto :goto_0

    :cond_3
    iget-object v1, p0, Lpmsj/work/e/s;->aa:[I

    aget v0, v1, v0

    invoke-static {v0}, Lpmsj/work/e/s;->D(I)V

    goto :goto_0

    :cond_4
    iget v1, p0, Lpmsj/work/e/s;->I:I

    if-ne v4, v1, :cond_0

    iget-object v1, p0, Lpmsj/work/e/s;->aa:[I

    aget v0, v1, v0

    invoke-static {v0}, Lpmsj/work/e/s;->C(I)V

    goto :goto_0
.end method

.method protected final c()V
    .locals 2

    const-string v0, "\u5bc4\u552e\u5546\u4eba"

    invoke-virtual {p0, v0}, Lpmsj/work/e/s;->d(Ljava/lang/String;)V

    const v0, 0x1155a

    invoke-virtual {p0, v0}, Lpmsj/work/e/s;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/g;

    iput-object v0, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    iget-object v0, p0, Lpmsj/work/e/s;->Z:Lpmsj/work/d/g;

    const/16 v1, 0x408

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->l(I)V

    return-void
.end method

.method public final y(I)V
    .locals 2

    const/16 v1, 0x472

    invoke-super {p0, p1}, Lpmsj/work/d/c;->y(I)V

    const/16 v0, 0xaf9

    if-ne p1, v0, :cond_1

    const/4 v0, 0x3

    invoke-static {v1, v0}, Lpmsj/work/main/w;->a(IB)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    const/16 v0, 0xafa

    if-ne p1, v0, :cond_0

    const/16 v0, 0x16

    invoke-static {v1, v0}, Lpmsj/work/main/w;->a(IB)V

    goto :goto_0
.end method
