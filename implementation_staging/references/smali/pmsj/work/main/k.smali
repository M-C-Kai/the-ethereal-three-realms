.class public final Lpmsj/work/main/k;
.super Lpmsj/work/d/c;


# static fields
.field public static a:[Ljava/lang/String;

.field private static final aD:La/b/c;

.field private static ad:Lpmsj/work/main/k;

.field public static b:J

.field public static c:I

.field public static d:I


# instance fields
.field private final K:I

.field private final L:I

.field private final M:I

.field private final N:I

.field private final O:I

.field private final P:I

.field private final Q:I

.field private final R:I

.field private final S:I

.field private final T:I

.field private U:Lpmsj/work/d/l;

.field private V:Lpmsj/work/d/g;

.field private W:Lpmsj/work/d/g;

.field private X:Lpmsj/work/d/a;

.field private Y:Lpmsj/work/d/a;

.field private Z:Lpmsj/work/d/a;

.field private aA:Ljava/lang/StringBuffer;

.field private final aB:I

.field private final aC:S

.field private final aE:S

.field private aF:Lpmsj/work/b/p;

.field private aG:Lpmsj/work/a/i;

.field private aH:Lpmsj/work/a/i;

.field private aI:Ljava/lang/StringBuffer;

.field private aJ:J

.field private aK:La/c/q;

.field private aL:I

.field private final aM:B

.field private aa:Lpmsj/work/d/a;

.field private ab:B

.field private ac:I

.field private ae:La/c/q;

.field private af:Lpmsj/work/a/i;

.field private ag:Lpmsj/work/d/d;

.field private ah:Lpmsj/work/d/d;

.field private ai:Lpmsj/work/d/d;

.field private aj:Lpmsj/work/d/d;

.field private ak:J

.field private al:Lpmsj/work/a/i;

.field private am:Lpmsj/work/d/a;

.field private an:Lpmsj/work/d/d;

.field private ao:Lpmsj/work/e/bs;

.field private ap:La/c/q;

.field private final aq:S

.field private ar:Lpmsj/work/main/x;

.field private as:Z

.field private at:Ljava/util/Vector;

.field private au:Lpmsj/work/a/i;

.field private av:Lpmsj/work/a/i;

.field private final aw:B

.field private final ax:B

.field private ay:Lpmsj/work/a/b;

.field private az:Lpmsj/work/a/b;

.field e:Lpmsj/work/main/l;

.field f:Lpmsj/work/a/i;


# direct methods
.method static constructor <clinit>()V
    .locals 3

    const/4 v2, 0x0

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    sput-wide v0, Lpmsj/work/main/k;->b:J

    const/4 v0, 0x1

    sput v0, Lpmsj/work/main/k;->c:I

    const/4 v0, 0x4

    sput v0, Lpmsj/work/main/k;->d:I

    new-instance v0, La/b/c;

    invoke-direct {v0, v2, v2}, La/b/c;-><init>(II)V

    sput-object v0, Lpmsj/work/main/k;->aD:La/b/c;

    return-void
.end method

.method private constructor <init>()V
    .locals 7

    const/4 v6, 0x1

    const v4, 0x54d8bb

    const/16 v3, 0x1e

    const/16 v2, 0x8

    const/4 v5, 0x0

    invoke-direct {p0}, Lpmsj/work/d/c;-><init>()V

    const/16 v0, 0xbbd

    iput v0, p0, Lpmsj/work/main/k;->K:I

    const/16 v0, 0xbc0

    iput v0, p0, Lpmsj/work/main/k;->L:I

    const/16 v0, 0xbc1

    iput v0, p0, Lpmsj/work/main/k;->M:I

    const/16 v0, 0xbc3

    iput v0, p0, Lpmsj/work/main/k;->N:I

    const/16 v0, 0xbc5

    iput v0, p0, Lpmsj/work/main/k;->O:I

    const/16 v0, 0xbc6

    iput v0, p0, Lpmsj/work/main/k;->P:I

    const/16 v0, 0xbc7

    iput v0, p0, Lpmsj/work/main/k;->Q:I

    const/16 v0, 0xbc8

    iput v0, p0, Lpmsj/work/main/k;->R:I

    const/16 v0, 0xbc9

    iput v0, p0, Lpmsj/work/main/k;->S:I

    const/16 v0, 0xbc2

    iput v0, p0, Lpmsj/work/main/k;->T:I

    const/4 v0, -0x1

    iput-byte v0, p0, Lpmsj/work/main/k;->ab:B

    new-instance v0, La/c/q;

    const/16 v1, 0x384

    invoke-direct {v0, v1}, La/c/q;-><init>(I)V

    iput-object v0, p0, Lpmsj/work/main/k;->ae:La/c/q;

    new-instance v0, Lpmsj/work/d/d;

    invoke-direct {v0, v3, v2, v4}, Lpmsj/work/d/d;-><init>(III)V

    iput-object v0, p0, Lpmsj/work/main/k;->ag:Lpmsj/work/d/d;

    new-instance v0, Lpmsj/work/d/d;

    invoke-direct {v0, v3, v2, v4}, Lpmsj/work/d/d;-><init>(III)V

    iput-object v0, p0, Lpmsj/work/main/k;->ah:Lpmsj/work/d/d;

    new-instance v0, Lpmsj/work/d/d;

    invoke-direct {v0, v3, v2, v4}, Lpmsj/work/d/d;-><init>(III)V

    iput-object v0, p0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x5991b0

    invoke-direct {v0, v1}, Lpmsj/work/a/i;-><init>(I)V

    iput-object v0, p0, Lpmsj/work/main/k;->al:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/d/d;

    invoke-direct {v0, v3, v2, v4}, Lpmsj/work/d/d;-><init>(III)V

    iput-object v0, p0, Lpmsj/work/main/k;->an:Lpmsj/work/d/d;

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/k;->ap:La/c/q;

    const/16 v0, 0xbb8

    iput-short v0, p0, Lpmsj/work/main/k;->aq:S

    invoke-static {v5}, Lpmsj/work/main/x;->a(B)Lpmsj/work/main/x;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/main/k;->ar:Lpmsj/work/main/x;

    new-instance v0, Ljava/util/Vector;

    invoke-direct {v0}, Ljava/util/Vector;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x553101

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/main/k;->au:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x553101

    invoke-direct {v0, v1, v6}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/main/k;->av:Lpmsj/work/a/i;

    const/16 v0, 0x20

    iput-byte v0, p0, Lpmsj/work/main/k;->aw:B

    const/16 v0, 0x12

    iput-byte v0, p0, Lpmsj/work/main/k;->ax:B

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    const-string v1, "\u53cc"

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/main/k;->aB:I

    const/16 v0, 0x100

    iput-short v0, p0, Lpmsj/work/main/k;->aC:S

    const/16 v0, 0x40

    iput-short v0, p0, Lpmsj/work/main/k;->aE:S

    new-instance v0, Lpmsj/work/b/p;

    const/16 v1, 0x100

    sget-object v2, Lpmsj/work/main/k;->aD:La/b/c;

    const/16 v3, 0x40

    const/16 v4, 0x40

    invoke-direct/range {v0 .. v5}, Lpmsj/work/b/p;-><init>(ILa/b/c;SSZ)V

    iput-object v0, p0, Lpmsj/work/main/k;->aF:Lpmsj/work/b/p;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x83595

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/main/k;->aG:Lpmsj/work/a/i;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x83595

    invoke-direct {v0, v1, v6}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/main/k;->aH:Lpmsj/work/a/i;

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x3666c

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/main/k;->f:Lpmsj/work/a/i;

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iput-wide v0, p0, Lpmsj/work/main/k;->aJ:J

    iput-byte v6, p0, Lpmsj/work/main/k;->aM:B

    return-void
.end method

.method private static C(I)V
    .locals 5

    const/4 v4, 0x0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ab()Z

    move-result v1

    if-eqz v1, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual {v0}, Lpmsj/work/b/ab;->M()Z

    move-result v1

    if-eqz v1, :cond_4

    invoke-virtual {v0}, Lpmsj/work/b/ab;->K()Z

    move-result v1

    if-eqz v1, :cond_0

    invoke-static {p0}, Lpmsj/work/main/k;->D(I)Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->M()Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->I()V

    iget v1, v0, Lpmsj/work/b/ab;->S:I

    if-eqz v1, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    iget v2, v0, Lpmsj/work/b/ab;->S:I

    invoke-virtual {v1, v2}, Lpmsj/work/b/m;->l(I)Lpmsj/work/b/t;

    move-result-object v1

    if-eqz v1, :cond_2

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    iget v3, v0, Lpmsj/work/b/ab;->S:I

    invoke-virtual {v2, v3}, Lpmsj/work/b/m;->e(I)V

    invoke-static {v1}, Lpmsj/work/main/k;->a(Lpmsj/work/b/n;)V

    :cond_2
    iput v4, v0, Lpmsj/work/b/ab;->S:I

    goto :goto_0

    :cond_3
    iget v1, v0, Lpmsj/work/b/ab;->T:I

    if-eqz v1, :cond_0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    iget v2, v0, Lpmsj/work/b/ab;->T:I

    invoke-virtual {v1, v2}, Lpmsj/work/b/m;->l(I)Lpmsj/work/b/t;

    move-result-object v1

    if-eqz v1, :cond_0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    iget v3, v0, Lpmsj/work/b/ab;->T:I

    invoke-virtual {v2, v3}, Lpmsj/work/b/m;->e(I)V

    invoke-static {v1}, Lpmsj/work/main/k;->a(Lpmsj/work/b/n;)V

    iput v4, v0, Lpmsj/work/b/ab;->T:I

    goto :goto_0

    :cond_4
    invoke-static {p0}, Lpmsj/work/main/k;->D(I)Z

    move-result v1

    if-nez v1, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->K()Z

    goto :goto_0
.end method

.method private static D(I)Z
    .locals 9

    const/4 v7, 0x0

    const/4 v6, -0x1

    const/4 v5, 0x1

    if-nez p0, :cond_0

    move v0, v7

    :goto_0
    return v0

    :cond_0
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-byte v0, v0, Lpmsj/work/b/ab;->e:B

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    iget-byte v1, v1, Lpmsj/work/b/ab;->f:B

    sget-object v2, Lpmsj/work/a/c;->Z:[S

    const/4 v3, 0x4

    aget-short v2, v2, v3

    if-ne v2, p0, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v0, v5

    sub-int v4, v1, v5

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_1

    sub-int/2addr v0, v5

    sub-int/2addr v1, v5

    move v8, v1

    move v1, v0

    move v0, v8

    :goto_1
    if-eq v6, v1, :cond_c

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2, v1, v0, v7}, Lpmsj/work/b/ab;->d(IIZ)Z

    move-result v0

    goto :goto_0

    :cond_1
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v1, v5

    invoke-virtual {v2, v0, v3}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_2

    sub-int/2addr v1, v5

    move v8, v1

    move v1, v0

    move v0, v8

    goto :goto_1

    :cond_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v0, v5

    invoke-virtual {v2, v3, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_d

    sub-int/2addr v0, v5

    move v8, v1

    move v1, v0

    move v0, v8

    goto :goto_1

    :cond_3
    sget-object v2, Lpmsj/work/a/c;->Z:[S

    const/4 v3, 0x5

    aget-short v2, v2, v3

    if-ne v2, p0, :cond_6

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v0, 0x1

    add-int/lit8 v4, v1, 0x1

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_4

    add-int/lit8 v0, v0, 0x1

    add-int/lit8 v1, v1, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto :goto_1

    :cond_4
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v0, 0x1

    invoke-virtual {v2, v3, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_5

    add-int/lit8 v0, v0, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto :goto_1

    :cond_5
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v1, 0x1

    invoke-virtual {v2, v0, v3}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_d

    add-int/lit8 v1, v1, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto :goto_1

    :cond_6
    sget-object v2, Lpmsj/work/a/c;->Z:[S

    const/4 v3, 0x3

    aget-short v2, v2, v3

    if-ne v2, p0, :cond_9

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v0, 0x1

    sub-int v4, v1, v5

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_7

    add-int/lit8 v0, v0, 0x1

    sub-int/2addr v1, v5

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_7
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v1, v5

    invoke-virtual {v2, v0, v3}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_8

    sub-int/2addr v1, v5

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_8
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v0, 0x1

    invoke-virtual {v2, v3, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_d

    add-int/lit8 v0, v0, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_9
    sget-object v2, Lpmsj/work/a/c;->Z:[S

    const/4 v3, 0x2

    aget-short v2, v2, v3

    if-ne v2, p0, :cond_d

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v0, v5

    add-int/lit8 v4, v1, 0x1

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_a

    sub-int/2addr v0, v5

    add-int/lit8 v1, v1, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_a
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    sub-int v3, v0, v5

    invoke-virtual {v2, v3, v1}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_b

    sub-int/2addr v0, v5

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_b
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    add-int/lit8 v3, v1, 0x1

    invoke-virtual {v2, v0, v3}, Lpmsj/work/b/m;->b(II)Z

    move-result v2

    if-nez v2, :cond_d

    add-int/lit8 v1, v1, 0x1

    move v8, v1

    move v1, v0

    move v0, v8

    goto/16 :goto_1

    :cond_c
    move v0, v7

    goto/16 :goto_0

    :cond_d
    move v0, v6

    move v1, v6

    goto/16 :goto_1
.end method

.method public static a()Lpmsj/work/main/k;
    .locals 3

    sget-object v0, Lpmsj/work/main/k;->ad:Lpmsj/work/main/k;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/main/k;

    invoke-direct {v0}, Lpmsj/work/main/k;-><init>()V

    sput-object v0, Lpmsj/work/main/k;->ad:Lpmsj/work/main/k;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x3

    sget-object v2, Lpmsj/work/main/k;->ad:Lpmsj/work/main/k;

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/d/c;)V

    :cond_0
    sget-object v0, Lpmsj/work/main/k;->ad:Lpmsj/work/main/k;

    return-object v0
.end method

.method public static a(Lpmsj/work/b/n;)V
    .locals 4

    const/4 v0, 0x6

    invoke-virtual {p0}, Lpmsj/work/b/n;->u()I

    move-result v1

    iget-byte v2, p0, Lpmsj/work/b/n;->e:B

    int-to-short v2, v2

    iget-byte v3, p0, Lpmsj/work/b/n;->f:B

    int-to-short v3, v3

    invoke-static {v0, v1, v2, v3}, Lpmsj/work/main/e;->a(IISS)V

    const/4 v0, 0x1

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lpmsj/work/main/t;->a(ZZ)V

    return-void
.end method

.method public static a_()V
    .locals 1

    const/4 v0, 0x0

    sput-object v0, Lpmsj/work/main/k;->ad:Lpmsj/work/main/k;

    return-void
.end method

.method private ap()Ljava/lang/String;
    .locals 6

    const/16 v5, 0x30

    const/16 v4, 0xc

    const/16 v2, 0xb

    const/4 v3, 0x2

    iget-object v0, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    invoke-static {}, Ljava/util/TimeZone;->getDefault()Ljava/util/TimeZone;

    move-result-object v0

    invoke-static {v0}, Ljava/util/Calendar;->getInstance(Ljava/util/TimeZone;)Ljava/util/Calendar;

    move-result-object v0

    invoke-virtual {v0, v2}, Ljava/util/Calendar;->get(I)I

    move-result v1

    invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v1

    if-ge v1, v3, :cond_0

    iget-object v1, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    invoke-virtual {v1, v5}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    :cond_0
    iget-object v1, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    invoke-virtual {v0, v2}, Ljava/util/Calendar;->get(I)I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    const/16 v2, 0x3a

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {v0, v4}, Ljava/util/Calendar;->get(I)I

    move-result v1

    invoke-static {v1}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->length()I

    move-result v1

    if-ge v1, v3, :cond_1

    iget-object v1, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    invoke-virtual {v1, v5}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    :cond_1
    iget-object v1, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    invoke-virtual {v0, v4}, Ljava/util/Calendar;->get(I)I

    move-result v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->aA:Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method private aq()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/k;->aF:Lpmsj/work/b/p;

    invoke-virtual {v0}, Lpmsj/work/b/p;->c()V

    iget-object v0, p0, Lpmsj/work/main/k;->aF:Lpmsj/work/b/p;

    invoke-virtual {v0}, Lpmsj/work/b/p;->a()V

    return-void
.end method

.method private ar()V
    .locals 11

    const/4 v9, 0x2

    const/16 v8, 0x1e

    const/4 v7, 0x1

    const/4 v6, 0x0

    const-string v10, "\u6218\u6597"

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->g()Lpmsj/work/b/n;

    move-result-object v2

    if-nez v2, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    new-instance v3, Ljava/util/Vector;

    invoke-direct {v3, v9}, Ljava/util/Vector;-><init>(I)V

    invoke-virtual {v2}, Lpmsj/work/b/n;->u()I

    move-result v4

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v4}, Lpmsj/work/b/m;->e(I)V

    instance-of v1, v2, Lpmsj/work/b/t;

    if-eqz v1, :cond_2

    invoke-virtual {v2}, Lpmsj/work/b/n;->u()I

    move-result v1

    iget-byte v3, v2, Lpmsj/work/b/n;->e:B

    int-to-short v3, v3

    iget-byte v2, v2, Lpmsj/work/b/n;->f:B

    int-to-short v2, v2

    invoke-static {v6, v1, v3, v2}, Lpmsj/work/main/e;->a(IISS)V

    invoke-static {v7, v6}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :cond_2
    instance-of v1, v2, Lpmsj/work/b/v;

    if-eqz v1, :cond_11

    move-object v0, v2

    check-cast v0, Lpmsj/work/b/v;

    move-object v1, v0

    sput-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    const/high16 v5, 0x80000

    invoke-virtual {v1, v5}, Lpmsj/work/b/m;->f(I)Z

    move-result v1

    if-eqz v1, :cond_4

    const-string v1, "\u67e5\u770b"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u6218\u6597"

    invoke-virtual {v3, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v3, p0, v7, v6}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;IZ)V

    :cond_3
    :goto_1
    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v1

    if-eqz v1, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v3, p0, v7, v7}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;IZ)V

    goto :goto_0

    :cond_4
    const/16 v1, 0x8

    invoke-virtual {v2, v1}, Lpmsj/work/b/n;->a(I)Z

    move-result v1

    if-eqz v1, :cond_5

    const-string v1, "\u644a\u4f4d"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_5
    const-string v1, "\u67e5\u770b"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u79c1\u804a"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u4ea4\u6613"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "\u8d60\u9001"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {v4}, Lpmsj/work/b/f;->b(I)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u52a0\u53cb"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_6
    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->c()I

    move-result v1

    if-lt v1, v8, :cond_a

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->c()I

    move-result v1

    if-ge v1, v8, :cond_a

    const-string v1, "\u6536\u5f92"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_7
    :goto_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    const/16 v5, 0x1000

    invoke-virtual {v1, v5}, Lpmsj/work/b/m;->f(I)Z

    move-result v1

    if-eqz v1, :cond_b

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->Z()Z

    move-result v1

    if-eqz v1, :cond_8

    const-string v1, "\u6bd4\u6b66"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_8
    :goto_3
    const/high16 v1, 0x20000

    invoke-virtual {v2, v1}, Lpmsj/work/b/n;->a(I)Z

    move-result v1

    if-eqz v1, :cond_9

    const-string v1, "\u89c2\u6218"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_9
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v3, p0, v9, v6}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;IZ)V

    goto/16 :goto_0

    :cond_a
    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->c()I

    move-result v1

    if-ge v1, v8, :cond_7

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->c()I

    move-result v1

    if-lt v1, v8, :cond_7

    const-string v1, "\u62dc\u5e08"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_2

    :cond_b
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    const/high16 v5, 0x400000

    invoke-virtual {v1, v5}, Lpmsj/work/b/m;->f(I)Z

    move-result v1

    if-nez v1, :cond_8

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    const/high16 v5, 0x200000

    invoke-virtual {v1, v5}, Lpmsj/work/b/m;->f(I)Z

    move-result v1

    if-nez v1, :cond_8

    invoke-static {v4}, Lpmsj/work/b/aa;->c(I)Z

    move-result v1

    if-nez v1, :cond_c

    const-string v1, "\u5207\u78cb"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v1, "PK"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_c
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->aa()Z

    move-result v1

    if-eqz v1, :cond_e

    invoke-static {}, Lpmsj/work/b/aa;->c()I

    move-result v1

    if-ne v1, v4, :cond_8

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->ab()Z

    move-result v1

    if-eqz v1, :cond_d

    const-string v1, "\u6682\u79bb"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_3

    :cond_d
    const-string v1, "\u5f52\u961f"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_3

    :cond_e
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->Z()Z

    move-result v1

    if-eqz v1, :cond_10

    invoke-static {v4}, Lpmsj/work/b/aa;->c(I)Z

    move-result v1

    if-eqz v1, :cond_f

    const-string v1, "\u4ea4\u961f"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_3

    :cond_f
    invoke-static {}, Lpmsj/work/b/aa;->a()Z

    move-result v1

    if-nez v1, :cond_8

    :cond_10
    const-string v1, "\u7ec4\u961f"

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_3

    :cond_11
    instance-of v1, v2, Lpmsj/work/b/q;

    if-eqz v1, :cond_12

    const-string v1, "\u6218\u6597"

    invoke-virtual {v3, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_1

    :cond_12
    instance-of v1, v2, Lpmsj/work/b/i;

    if-eqz v1, :cond_3

    check-cast v2, Lpmsj/work/b/i;

    const/16 v1, 0x9

    invoke-virtual {v2, v1}, Lpmsj/work/b/i;->j(B)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_1
.end method

.method private as()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->setLength(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    const-string v1, "["

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v1, v1, Lpmsj/work/b/ab;->e:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    const-string v1, ", "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v1, v1, Lpmsj/work/b/ab;->f:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    const-string v1, "]"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    iget-object v0, p0, Lpmsj/work/main/k;->Y:Lpmsj/work/d/a;

    iget-object v1, p0, Lpmsj/work/main/k;->aI:Ljava/lang/StringBuffer;

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->a_(Ljava/lang/String;)V

    return-void
.end method

.method private at()V
    .locals 3

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->m()V

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    sget-short v1, Lpmsj/work/main/t;->d:S

    iget-object v2, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->l:I

    sub-int/2addr v1, v2

    const/16 v2, 0x23

    sub-int/2addr v1, v2

    const/16 v2, 0x14

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    return-void
.end method

.method private static b(Lpmsj/work/d/c;)V
    .locals 2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x17d

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ap;

    invoke-virtual {p0, v0}, Lpmsj/work/d/c;->a(Lpmsj/work/d/c;)V

    if-eqz v0, :cond_0

    const/4 v1, 0x0

    invoke-virtual {v0, v1}, Lpmsj/work/e/ap;->a(Z)V

    :cond_0
    return-void
.end method

.method public static q()V
    .locals 2

    const/4 v1, 0x0

    const/16 v0, 0x3eb

    invoke-static {v0, v1}, Lpmsj/work/main/w;->b(II)V

    sput-byte v1, Lpmsj/work/main/i;->b:B

    const-wide/16 v0, 0x3e8

    :try_start_0
    invoke-static {v0, v1}, Ljava/lang/Thread;->sleep(J)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    :goto_0
    const-string v0, ""

    invoke-static {v0}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    return-void

    :catch_0
    move-exception v0

    goto :goto_0
.end method


# virtual methods
.method public final a(BIIIIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;)V
    .locals 14

    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/main/l;

    invoke-direct {v0, p0}, Lpmsj/work/main/l;-><init>(Lpmsj/work/main/k;)V

    iput-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    :cond_0
    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iput-byte p1, v0, Lpmsj/work/main/l;->a:B

    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v0, v0, Lpmsj/work/main/l;->b:[I

    const/4 v1, 0x0

    aput p3, v0, v1

    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v0, v0, Lpmsj/work/main/l;->b:[I

    const/4 v1, 0x1

    aput p4, v0, v1

    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v0, v0, Lpmsj/work/main/l;->b:[I

    const/4 v1, 0x2

    aput p5, v0, v1

    iget-object v0, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v0, v0, Lpmsj/work/main/l;->b:[I

    const/4 v1, 0x3

    aput p6, v0, v1

    invoke-virtual/range {p8 .. p8}, Ljava/lang/String;->length()I

    move-result v0

    if-gtz v0, :cond_3

    const-string v0, "\u786e\u5b9a"

    move-object v4, v0

    :goto_0
    invoke-virtual/range {p9 .. p9}, Ljava/lang/String;->length()I

    move-result v0

    if-gtz v0, :cond_2

    const-string v0, "\u8fd4\u56de"

    move-object v5, v0

    :goto_1
    packed-switch p2, :pswitch_data_0

    :cond_1
    :goto_2
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v2, 0x63

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v3

    move-object/from16 v1, p7

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    goto :goto_2

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v2, 0x63

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v3

    move-object/from16 v1, p7

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    goto :goto_2

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v6

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v9

    const-string v11, "\u8bf7\u8f93\u5165\u6570\u636e"

    const-string v13, ""

    const/16 v8, 0x64

    const/16 v10, 0x14

    const/4 v12, 0x0

    move-object/from16 v7, p7

    invoke-virtual/range {v6 .. v13}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/aa;

    if-eqz p0, :cond_1

    invoke-virtual {p0, v4, v5}, Lpmsj/work/e/aa;->a(Ljava/lang/String;Ljava/lang/String;)V

    goto :goto_2

    :cond_2
    move-object/from16 v5, p9

    goto :goto_1

    :cond_3
    move-object/from16 v4, p8

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method protected final a(II)V
    .locals 4

    const/4 v2, 0x0

    const/4 v3, 0x1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->L:La/b/c;

    if-eqz v0, :cond_0

    :goto_0
    return-void

    :cond_0
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0, p1, p2}, Lpmsj/work/b/m;->l(II)Ljava/util/Vector;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ne v0, v3, :cond_1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->a(Lpmsj/work/b/n;)V

    invoke-direct {p0}, Lpmsj/work/main/k;->ar()V

    goto :goto_0

    :cond_1
    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-le v0, v3, :cond_3

    new-instance v1, Ljava/util/Vector;

    invoke-direct {v1}, Ljava/util/Vector;-><init>()V

    :goto_1
    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v2, v0, :cond_2

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v0, v2, 0x1

    int-to-byte v0, v0

    move v2, v0

    goto :goto_1

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1, p0, v3, v3}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;IZ)V

    goto :goto_0

    :cond_3
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0, p1, p2}, Lpmsj/work/b/m;->i(II)La/b/c;

    move-result-object v0

    iget-short v1, v0, La/b/c;->a:S

    iget-short v0, v0, La/b/c;->b:S

    invoke-static {v1, v0, v2}, Lpmsj/work/main/c;->a(IIZ)V

    goto :goto_0
.end method

.method public final a(Ljava/lang/String;Ljava/lang/String;)V
    .locals 3

    const/4 v2, 0x2

    const/4 v1, 0x1

    iget-object v0, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    invoke-virtual {v0, p1, v1, v2}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    iget-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    invoke-virtual {v0, p2, v1, v2}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    return-void
.end method

.method public final a(Ljava/lang/StringBuffer;)V
    .locals 2

    sget v0, Lpmsj/work/main/k;->c:I

    const/4 v1, 0x1

    if-ne v0, v1, :cond_0

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    sget v1, Lpmsj/work/main/k;->c:I

    add-int/lit8 v1, v1, 0x1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->t(I)V

    :cond_0
    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    invoke-virtual {p1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iput-wide v0, p0, Lpmsj/work/main/k;->aJ:J

    invoke-direct {p0}, Lpmsj/work/main/k;->at()V

    return-void
.end method

.method protected final a(Ljavax/microedition/lcdui/Graphics;)V
    .locals 0

    return-void
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 6

    const/16 v5, 0x23

    invoke-super {p0, p1, p2, p3}, Lpmsj/work/d/c;->a(Ljavax/microedition/lcdui/Graphics;II)V

    sget-boolean v0, Lpmsj/work/main/t;->v:Z

    if-nez v0, :cond_0

    sget-boolean v0, Lpmsj/work/main/t;->w:Z

    if-eqz v0, :cond_2

    :cond_0
    sget-short v0, Lpmsj/work/main/t;->d:S

    sub-int/2addr v0, v5

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v1

    sget-wide v3, Lpmsj/work/main/k;->b:J

    sub-long/2addr v1, v3

    const-wide/16 v3, 0x190

    cmp-long v1, v1, v3

    if-lez v1, :cond_1

    sget-short v1, Lpmsj/work/main/t;->c:S

    sget-byte v2, Lpmsj/work/main/k;->E:B

    sub-int/2addr v1, v2

    const/16 v2, 0x8

    sub-int/2addr v1, v2

    add-int/lit8 v1, v1, 0x1

    const/4 v2, 0x5

    sub-int v2, v1, v2

    sget-byte v3, Lpmsj/work/main/k;->E:B

    add-int/lit8 v3, v3, 0xa

    const/4 v4, 0x1

    invoke-static {p1, v2, v0, v3, v4}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIB)V

    const-string v2, "\u64cd\u4f5c"

    sget v3, Lpmsj/work/a/c;->ac:I

    sub-int v3, v5, v3

    div-int/lit8 v3, v3, 0x2

    add-int/2addr v0, v3

    const v3, 0xf8f8a0

    invoke-static {p1, v2, v1, v0, v3}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V

    :cond_1
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    sget-wide v2, Lpmsj/work/main/k;->b:J

    sub-long/2addr v0, v2

    const-wide/16 v2, 0x320

    cmp-long v0, v0, v2

    if-lez v0, :cond_2

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    sput-wide v0, Lpmsj/work/main/k;->b:J

    :cond_2
    return-void
.end method

.method protected final a(Lpmsj/work/d/b;)V
    .locals 2

    iget v0, p1, Lpmsj/work/d/b;->g:I

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    check-cast p1, Lpmsj/work/d/g;

    invoke-virtual {p1}, Lpmsj/work/d/g;->f()I

    move-result v0

    int-to-byte v0, v0

    iput-byte v0, p0, Lpmsj/work/main/k;->ab:B

    iget-object v0, p0, Lpmsj/work/main/k;->ar:Lpmsj/work/main/x;

    iget-byte v1, p0, Lpmsj/work/main/k;->ab:B

    invoke-virtual {v0, v1}, Lpmsj/work/main/x;->b(I)Z

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0xbbd
        :pswitch_0
    .end packed-switch
.end method

.method public final a([La/c/i;B)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0, p1, p2}, Lpmsj/work/e/bs;->a([La/c/i;B)V

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lpmsj/work/e/bs;->a(Z)V

    return-void
.end method

.method public final a(ILjava/lang/String;)Z
    .locals 10

    const/4 v9, 0x1

    if-ne p1, v9, :cond_1

    invoke-virtual {p2}, Ljava/lang/String;->length()I

    move-result v0

    if-lez v0, :cond_0

    const/16 v0, 0x7db

    new-instance v1, Ljava/lang/StringBuffer;

    invoke-direct {v1, p2}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v2, ""

    sget-object v3, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v3}, Lpmsj/work/b/ab;->p()Ljava/lang/String;

    move-result-object v3

    invoke-static {v0, v1, v2, v3}, Lpmsj/work/main/e;->a(SLjava/lang/StringBuffer;Ljava/lang/String;Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*2\u60a8\u7684\u5efa\u8bae\u5df2\u7ecf\u63d0\u4ea4\u5230GM,\u5982\u679c\u60a8\u7684\u5efa\u8bae\u88ab\u91c7\u7eb3\u60a8\u5c06\u4f1a\u5f97\u5230\u4e30\u539a\u7684\u5956\u52b1\u3002"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    :cond_0
    :goto_0
    return v9

    :cond_1
    const/16 v0, 0x64

    if-ne p1, v0, :cond_0

    const/16 v0, 0x5e5

    new-instance v1, La/c/h;

    iget-object v2, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-byte v2, v2, Lpmsj/work/main/l;->a:B

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/h;

    invoke-direct {v2, v9}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    iget-object v4, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v4, v4, Lpmsj/work/main/l;->b:[I

    const/4 v5, 0x0

    aget v4, v4, v5

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    iget-object v5, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v5, v5, Lpmsj/work/main/l;->b:[I

    aget v5, v5, v9

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    iget-object v6, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v6, v6, Lpmsj/work/main/l;->b:[I

    const/4 v7, 0x2

    aget v6, v6, v7

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    iget-object v7, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v7, v7, Lpmsj/work/main/l;->b:[I

    const/4 v8, 0x3

    aget v7, v7, v8

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    new-instance v7, La/c/p;

    invoke-direct {v7, p2}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static/range {v0 .. v7}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto :goto_0
.end method

.method public final a(Lpmsj/work/b/j;)Z
    .locals 4

    const/16 v0, 0x3f1

    const/16 v1, 0x51

    iget v2, p1, Lpmsj/work/b/j;->e:I

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v2, v3}, Lpmsj/work/main/w;->a(ISII)V

    const/4 v0, 0x0

    return v0
.end method

.method public final a_(II)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/main/k;->aK:La/c/q;

    if-nez v0, :cond_0

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/main/k;->aK:La/c/q;

    :cond_0
    iget-object v0, p0, Lpmsj/work/main/k;->aK:La/c/q;

    mul-int/lit16 v1, p1, 0x3e8

    invoke-virtual {v0, v1}, La/c/q;->e(I)V

    iput p2, p0, Lpmsj/work/main/k;->aL:I

    return-void
.end method

.method public final a_(I)Z
    .locals 4

    const/16 v3, 0x9

    const/4 v2, -0x1

    const/16 v1, 0xa

    iput-byte v2, p0, Lpmsj/work/main/k;->ab:B

    if-lt p1, v1, :cond_1

    sub-int v0, p1, v1

    int-to-byte v0, v0

    iput-byte v0, p0, Lpmsj/work/main/k;->ab:B

    :cond_0
    :goto_0
    iget-byte v0, p0, Lpmsj/work/main/k;->ab:B

    if-eq v2, v0, :cond_4

    iget-object v0, p0, Lpmsj/work/main/k;->ar:Lpmsj/work/main/x;

    iget-byte v1, p0, Lpmsj/work/main/k;->ab:B

    invoke-virtual {v0, v1}, Lpmsj/work/main/x;->b(I)Z

    move-result v0

    :goto_1
    return v0

    :cond_1
    const/4 v0, 0x7

    if-ne v0, p1, :cond_2

    iput-byte v3, p0, Lpmsj/work/main/k;->ab:B

    goto :goto_0

    :cond_2
    if-ne v3, p1, :cond_3

    iput-byte v1, p0, Lpmsj/work/main/k;->ab:B

    goto :goto_0

    :cond_3
    const/16 v0, 0x8

    if-ne v0, p1, :cond_0

    const/16 v0, 0xb

    iput-byte v0, p0, Lpmsj/work/main/k;->ab:B

    goto :goto_0

    :cond_4
    const/4 v0, 0x0

    goto :goto_1
.end method

.method protected final b(Ljavax/microedition/lcdui/Graphics;)V
    .locals 0

    return-void
.end method

.method public final b(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 33

    :try_start_0
    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-eqz v5, :cond_4

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sget-wide v7, Lpmsj/work/main/k;->b:J

    sub-long/2addr v5, v7

    const-wide/16 v7, 0x190

    cmp-long v5, v5, v7

    if-lez v5, :cond_4

    const/16 v5, 0x37

    sget-boolean v6, Lpmsj/work/main/f;->g:Z

    if-eqz v6, :cond_0

    const/16 v5, 0x41

    :cond_0
    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v6

    iget-boolean v6, v6, Lpmsj/work/main/d;->e:Z

    if-eqz v6, :cond_1b

    const v6, 0x594390

    invoke-static {v6}, La/a/f;->a(I)La/a/e;

    move-result-object v6

    if-eqz v6, :cond_1

    sget-short v7, Lpmsj/work/main/t;->c:S

    const/16 v8, 0x14

    sub-int/2addr v7, v8

    move-object v0, v6

    move-object/from16 v1, p1

    move v2, v7

    move v3, v5

    invoke-virtual {v0, v1, v2, v3}, La/a/e;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_1
    add-int/lit8 v5, v5, 0xe

    int-to-short v5, v5

    move v8, v5

    :goto_0
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sget-wide v9, Lpmsj/work/main/k;->b:J

    sub-long/2addr v5, v9

    const-wide/16 v9, 0x320

    cmp-long v5, v5, v9

    if-lez v5, :cond_2

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sput-wide v5, Lpmsj/work/main/k;->b:J

    :cond_2
    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/high16 v6, 0x4000000

    invoke-virtual {v5, v6}, Lpmsj/work/b/ab;->a(I)Z

    move-result v5

    if-eqz v5, :cond_3

    const-string v6, "\u53cc"

    sget-short v5, Lpmsj/work/main/t;->c:S

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/main/k;->aB:I

    move v7, v0

    shl-int/lit8 v7, v7, 0x1

    sub-int v7, v5, v7

    sget-object v9, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    sget v10, Lpmsj/work/a/c;->y:I

    sget v11, Lpmsj/work/a/c;->B:I

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v11}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    :cond_3
    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/high16 v6, 0x8000000

    invoke-virtual {v5, v6}, Lpmsj/work/b/ab;->a(I)Z

    move-result v5

    if-eqz v5, :cond_4

    const-string v6, "\u53cc"

    sget-short v5, Lpmsj/work/main/t;->c:S

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/main/k;->aB:I

    move v7, v0

    sub-int v7, v5, v7

    sget-object v9, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    sget v10, Lpmsj/work/a/c;->y:I

    sget v11, Lpmsj/work/a/c;->C:I

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v11}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    :cond_4
    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-eqz v5, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ag:Lpmsj/work/d/d;

    move-object v6, v0

    const/16 v7, 0xb

    invoke-virtual {v5, v7}, Lpmsj/work/b/ab;->f(B)I

    move-result v7

    invoke-virtual {v6, v7}, Lpmsj/work/d/d;->a(I)V

    const v6, 0x5fac30

    invoke-static {v6}, La/a/f;->a(I)La/a/e;

    move-result-object v6

    const/4 v7, 0x0

    const/4 v8, 0x0

    const/4 v9, 0x0

    move-object v0, v6

    move-object/from16 v1, p1

    move v2, v7

    move v3, v8

    move v4, v9

    invoke-virtual {v0, v1, v2, v3, v4}, La/a/e;->a(Ljavax/microedition/lcdui/Graphics;III)V

    invoke-virtual {v6}, La/a/e;->a()I

    move-result v7

    const/16 v8, 0x28

    sub-int/2addr v7, v8

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->au:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v9

    const/16 v10, 0x26

    sub-int/2addr v9, v10

    const/16 v10, 0x20

    const/16 v11, 0x29

    invoke-virtual {v5, v11}, Lpmsj/work/b/ab;->f(B)I

    move-result v11

    invoke-virtual {v5}, Lpmsj/work/b/ab;->w()I

    move-result v12

    invoke-static {v10, v11, v12}, La/c/x;->a(III)I

    move-result v10

    move-object v0, v8

    move v1, v7

    move v2, v9

    move v3, v10

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->av:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v9

    const/16 v10, 0x20

    sub-int/2addr v9, v10

    const/16 v10, 0x20

    const/16 v11, 0x2b

    invoke-virtual {v5, v11}, Lpmsj/work/b/ab;->f(B)I

    move-result v11

    invoke-virtual {v5}, Lpmsj/work/b/ab;->y()I

    move-result v12

    invoke-static {v10, v11, v12}, La/c/x;->a(III)I

    move-result v10

    move-object v0, v8

    move v1, v7

    move v2, v9

    move v3, v10

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->af:Lpmsj/work/a/i;

    move-object v7, v0

    if-eqz v7, :cond_5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->af:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v6}, La/a/e;->a()I

    move-result v8

    const/16 v9, 0x44

    sub-int/2addr v8, v9

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v9

    const/16 v10, 0x25

    sub-int/2addr v9, v10

    const/4 v10, 0x0

    move-object v0, v7

    move-object/from16 v1, p1

    move v2, v8

    move v3, v9

    move v4, v10

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    :cond_5
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ag:Lpmsj/work/d/d;

    move-object v7, v0

    const/4 v8, -0x1

    const/4 v9, -0x1

    move-object v0, v7

    move-object/from16 v1, p1

    move v2, v8

    move v3, v9

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    const/16 v7, 0x26

    invoke-virtual {v5, v7}, Lpmsj/work/b/ab;->f(B)I

    move-result v5

    if-lez v5, :cond_7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ay:Lpmsj/work/a/b;

    move-object v5, v0

    if-nez v5, :cond_6

    new-instance v5, Lpmsj/work/a/b;

    const v7, 0x596cfe

    invoke-direct {v5, v7}, Lpmsj/work/a/b;-><init>(I)V

    move-object v0, v5

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/main/k;->ay:Lpmsj/work/a/b;

    :cond_6
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ay:Lpmsj/work/a/b;

    move-object v5, v0

    invoke-virtual {v6}, La/a/e;->a()I

    move-result v7

    const/16 v8, 0x46

    sub-int/2addr v7, v8

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->af:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v7

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/a/b;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_7
    sget-object v5, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-eqz v5, :cond_9

    invoke-virtual {v6}, La/a/e;->a()I

    move-result v5

    const/16 v7, 0x19

    sub-int/2addr v5, v7

    sget-object v7, Lpmsj/work/b/v;->B:Lpmsj/work/a/i;

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v8

    const/16 v9, 0x17

    sub-int/2addr v8, v9

    const/16 v9, 0x12

    sget-object v10, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v11, 0x27

    invoke-virtual {v10, v11}, Lpmsj/work/b/u;->f(B)I

    move-result v10

    sget-object v11, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v12, 0x26

    invoke-virtual {v11, v12}, Lpmsj/work/b/u;->f(B)I

    move-result v11

    invoke-static {v9, v10, v11}, La/c/x;->a(III)I

    move-result v9

    move-object v0, v7

    move v1, v5

    move v2, v8

    move v3, v9

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    sget-object v7, Lpmsj/work/b/v;->C:Lpmsj/work/a/i;

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v8

    const/16 v9, 0x13

    sub-int/2addr v8, v9

    const/16 v9, 0x12

    sget-object v10, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v11, 0x29

    invoke-virtual {v10, v11}, Lpmsj/work/b/u;->f(B)I

    move-result v10

    sget-object v11, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v12, 0x28

    invoke-virtual {v11, v12}, Lpmsj/work/b/u;->f(B)I

    move-result v11

    invoke-static {v9, v10, v11}, La/c/x;->a(III)I

    move-result v9

    move-object v0, v7

    move v1, v5

    move v2, v8

    move v3, v9

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    sget-object v7, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v8, 0x1e

    invoke-virtual {v7, v8}, Lpmsj/work/b/u;->f(B)I

    move-result v7

    sget-object v8, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v9, 0x1f

    invoke-virtual {v8, v9}, Lpmsj/work/b/u;->f(B)I

    move-result v8

    if-lt v7, v8, :cond_10

    const/16 v7, 0x12

    :goto_1
    sget-object v8, Lpmsj/work/b/v;->D:Lpmsj/work/a/i;

    invoke-virtual {v6}, La/a/e;->b()I

    move-result v6

    const/16 v9, 0xf

    sub-int/2addr v6, v9

    move-object v0, v8

    move v1, v5

    move v2, v6

    move v3, v7

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ah:Lpmsj/work/d/d;

    move-object v5, v0

    sget-object v6, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/4 v7, 0x7

    invoke-virtual {v6, v7}, Lpmsj/work/b/u;->f(B)I

    move-result v6

    invoke-virtual {v5, v6}, Lpmsj/work/d/d;->a(I)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ah:Lpmsj/work/d/d;

    move-object v5, v0

    const/4 v6, -0x1

    const/4 v7, -0x1

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    sget-object v5, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v6, 0x25

    invoke-virtual {v5, v6}, Lpmsj/work/b/u;->f(B)I

    move-result v5

    if-lez v5, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->az:Lpmsj/work/a/b;

    move-object v5, v0

    if-nez v5, :cond_8

    new-instance v5, Lpmsj/work/a/b;

    const v6, 0x596cfe

    invoke-direct {v5, v6}, Lpmsj/work/a/b;-><init>(I)V

    move-object v0, v5

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/main/k;->az:Lpmsj/work/a/b;

    :cond_8
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->az:Lpmsj/work/a/b;

    move-object v5, v0

    const/16 v6, 0x2e

    const/16 v7, 0x19

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/a/b;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_9
    sget-boolean v5, Lpmsj/work/main/f;->g:Z

    if-eqz v5, :cond_b

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    move-object/from16 v0, p0

    iget-wide v0, v0, Lpmsj/work/main/k;->ak:J

    move-wide v7, v0

    sub-long/2addr v5, v7

    const-wide/32 v7, 0xea60

    cmp-long v5, v5, v7

    if-lez v5, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    move-object v5, v0

    invoke-direct/range {p0 .. p0}, Lpmsj/work/main/k;->ap()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Lpmsj/work/d/d;->b(Ljava/lang/String;)V

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    move-wide v0, v5

    move-object/from16 v2, p0

    iput-wide v0, v2, Lpmsj/work/main/k;->ak:J

    :cond_a
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->al:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    move-object v6, v0

    iget-short v6, v6, Lpmsj/work/d/d;->i:S

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->al:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->c()I

    move-result v7

    sub-int/2addr v6, v7

    const/4 v7, 0x1

    const/4 v8, 0x0

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    move-object v5, v0

    const/4 v6, -0x1

    const/4 v7, -0x1

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_b
    sget-boolean v5, Lpmsj/work/main/t;->v:Z

    if-nez v5, :cond_c

    sget-boolean v5, Lpmsj/work/main/t;->w:Z

    if-eqz v5, :cond_e

    :cond_c
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sget-wide v7, Lpmsj/work/main/k;->b:J

    sub-long/2addr v5, v7

    const-wide/16 v7, 0x190

    cmp-long v5, v5, v7

    if-lez v5, :cond_d

    const v5, 0x594390

    invoke-static {v5}, La/a/f;->a(I)La/a/e;

    move-result-object v5

    if-eqz v5, :cond_d

    sget-short v6, Lpmsj/work/main/t;->c:S

    const/16 v7, 0x14

    sub-int/2addr v6, v7

    const/16 v7, 0x37

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, La/a/e;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_d
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sget-wide v7, Lpmsj/work/main/k;->b:J

    sub-long/2addr v5, v7

    const-wide/16 v7, 0x320

    cmp-long v5, v5, v7

    if-lez v5, :cond_e

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    sput-wide v5, Lpmsj/work/main/k;->b:J

    :cond_e
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aK:La/c/q;

    move-object v5, v0

    if-eqz v5, :cond_f

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aK:La/c/q;

    move-object v5, v0

    invoke-virtual {v5}, La/c/q;->i()Z

    move-result v5

    if-eqz v5, :cond_11

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/main/k;->s()V

    :cond_f
    :goto_2
    sget-object v5, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v26

    const/4 v5, 0x1

    move/from16 v0, v26

    move v1, v5

    if-le v0, v1, :cond_14

    sget-object v5, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    sget-object v6, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v6}, Lpmsj/work/a/i;->c()I

    move-result v6

    mul-int/lit8 v6, v6, 0x3

    add-int/lit8 v6, v6, 0x2

    invoke-virtual {v5}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v7

    add-int/lit8 v7, v7, 0x3c

    const/4 v8, 0x0

    sub-int/2addr v7, v8

    sget-object v8, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    add-int/lit8 v8, v8, 0x0

    div-int/lit8 v8, v8, 0x2

    const/4 v9, 0x3

    if-le v8, v9, :cond_12

    const/4 v8, 0x3

    move v9, v8

    :goto_3
    mul-int/lit8 v8, v9, 0x2

    add-int v27, v7, v8

    invoke-virtual {v5}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v8

    add-int v8, v8, v27

    const/4 v10, 0x0

    sub-int v28, v8, v10

    invoke-virtual {v5}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v5

    mul-int/lit8 v8, v9, 0x2

    add-int/2addr v5, v8

    const/4 v8, 0x0

    sub-int v29, v5, v8

    invoke-static {}, Lpmsj/work/b/aa;->c()I

    move-result v30

    const/4 v5, 0x0

    const/4 v8, 0x0

    move/from16 v31, v8

    move/from16 v32, v5

    :goto_4
    move/from16 v0, v31

    move/from16 v1, v26

    if-ge v0, v1, :cond_14

    sget-object v5, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    move-object v0, v5

    move/from16 v1, v31

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v5

    move-object v0, v5

    check-cast v0, [La/c/i;

    move-object v8, v0

    invoke-static {v8}, Lpmsj/work/b/aa;->a([La/c/i;)I

    move-result v12

    const/4 v5, 0x0

    aget-object v5, v8, v5

    check-cast v5, La/c/p;

    invoke-virtual {v5}, La/c/p;->e()Ljava/lang/String;

    move-result-object v13

    const/4 v5, 0x3

    aget-object v5, v8, v5

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    const/4 v10, 0x2

    aget-object v10, v8, v10

    invoke-virtual {v10}, La/c/i;->b()I

    move-result v11

    if-le v5, v11, :cond_1a

    move v10, v11

    :goto_5
    const/4 v5, 0x5

    aget-object v5, v8, v5

    check-cast v5, La/c/o;

    iget-short v5, v5, La/c/o;->a:S

    const/4 v14, 0x6

    aget-object v14, v8, v14

    invoke-virtual {v14}, La/c/i;->b()I

    move-result v15

    const/4 v14, 0x7

    aget-object v8, v8, v14

    invoke-virtual {v8}, La/c/i;->b()I

    move-result v16

    move v0, v12

    move/from16 v1, v30

    if-ne v0, v1, :cond_13

    sget-object v8, Lpmsj/work/a/c;->v:[I

    const/4 v12, 0x3

    aget v8, v8, v12

    move-object/from16 v0, p1

    move v1, v8

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-static {v13}, La/c/x;->e(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    const/4 v12, 0x2

    const/16 v13, 0x3c

    const/16 v14, 0x14

    move-object/from16 v0, p1

    move-object v1, v8

    move v2, v12

    move v3, v13

    move v4, v14

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    new-instance v8, Lpmsj/work/d/d;

    const/16 v12, 0x1e

    const/16 v13, 0x8

    const v14, 0x54d8bb

    invoke-direct {v8, v12, v13, v14}, Lpmsj/work/d/d;-><init>(III)V

    invoke-virtual {v8, v5}, Lpmsj/work/d/d;->a(I)V

    const/4 v5, 0x2

    invoke-virtual {v8, v5, v7}, Lpmsj/work/d/d;->f(II)V

    const/4 v5, -0x1

    const/4 v12, -0x1

    move-object v0, v8

    move-object/from16 v1, p1

    move v2, v5

    move v3, v12

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    const/16 v8, 0x19

    sget-object v5, Lpmsj/work/a/c;->v:[I

    const/4 v12, 0x2

    aget v12, v5, v12

    const v13, 0x3e3e3e

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v13}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V

    add-int v12, v7, v9

    const/16 v13, 0x19

    sget-object v5, Lpmsj/work/a/c;->v:[I

    const/16 v8, 0x8

    aget v17, v5, v8

    const v18, 0x3e3e3e

    move-object/from16 v10, p1

    move v11, v6

    move v14, v9

    invoke-static/range {v10 .. v18}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V

    move/from16 v5, v32

    :goto_6
    add-int/lit8 v8, v31, 0x1

    move/from16 v31, v8

    move/from16 v32, v5

    goto/16 :goto_4

    :cond_10
    const/16 v9, 0x12

    invoke-static {v9, v8, v7}, La/c/x;->a(III)I

    move-result v7

    goto/16 :goto_1

    :cond_11
    sget-short v5, Lpmsj/work/main/t;->c:S

    const/16 v6, 0x64

    sub-int/2addr v5, v6

    shr-int/lit8 v6, v5, 0x1

    sget-short v5, Lpmsj/work/main/t;->d:S

    const/16 v7, 0x3c

    sub-int v7, v5, v7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aK:La/c/q;

    move-object v5, v0

    invoke-virtual {v5}, La/c/q;->k()I

    move-result v10

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aK:La/c/q;

    move-object v5, v0

    invoke-virtual {v5}, La/c/q;->j()I

    move-result v11

    const/16 v8, 0x64

    const/16 v9, 0x14

    const v12, 0xf4ff67

    sget-object v5, Lpmsj/work/a/c;->v:[I

    const/16 v13, 0xa

    aget v13, v5, v13

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v13}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    goto/16 :goto_2

    :catch_0
    move-exception v5

    invoke-virtual {v5}, Ljava/lang/Exception;->printStackTrace()V

    :goto_7
    return-void

    :cond_12
    :try_start_1
    sget-object v8, La/c/x;->f:Lpmsj/work/a/i;

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    add-int/lit8 v8, v8, 0x0

    div-int/lit8 v8, v8, 0x2

    move v9, v8

    goto/16 :goto_3

    :cond_13
    sget-object v8, Lpmsj/work/a/c;->v:[I

    const/4 v12, 0x0

    aget v8, v8, v12

    move-object/from16 v0, p1

    move v1, v8

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    invoke-static {v13}, La/c/x;->e(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    const/4 v12, 0x2

    mul-int v13, v29, v32

    add-int v13, v13, v27

    const/16 v14, 0x14

    move-object/from16 v0, p1

    move-object v1, v8

    move v2, v12

    move v3, v13

    move v4, v14

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->a(Ljava/lang/String;III)V

    new-instance v8, Lpmsj/work/d/d;

    const/16 v12, 0x1e

    const/16 v13, 0x8

    const v14, 0x54d8bb

    invoke-direct {v8, v12, v13, v14}, Lpmsj/work/d/d;-><init>(III)V

    invoke-virtual {v8, v5}, Lpmsj/work/d/d;->a(I)V

    const/4 v5, 0x2

    mul-int v12, v29, v32

    add-int v12, v12, v28

    invoke-virtual {v8, v5, v12}, Lpmsj/work/d/d;->f(II)V

    const/4 v5, -0x1

    const/4 v12, -0x1

    move-object v0, v8

    move-object/from16 v1, p1

    move v2, v5

    move v3, v12

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/d;->b(Ljavax/microedition/lcdui/Graphics;II)V

    mul-int v5, v29, v32

    add-int v19, v28, v5

    const/16 v20, 0x19

    sget-object v5, Lpmsj/work/a/c;->v:[I

    const/4 v8, 0x2

    aget v24, v5, v8

    const v25, 0x3e3e3e

    move-object/from16 v17, p1

    move/from16 v18, v6

    move/from16 v21, v9

    move/from16 v22, v10

    move/from16 v23, v11

    invoke-static/range {v17 .. v25}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V

    mul-int v5, v29, v32

    add-int v5, v5, v28

    add-int v12, v5, v9

    const/16 v13, 0x19

    sget-object v5, Lpmsj/work/a/c;->v:[I

    const/16 v8, 0x8

    aget v17, v5, v8

    const v18, 0x3e3e3e

    move-object/from16 v10, p1

    move v11, v6

    move v14, v9

    invoke-static/range {v10 .. v18}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIIIIII)V

    add-int/lit8 v5, v32, 0x1

    goto/16 :goto_6

    :cond_14
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v5

    iget-boolean v5, v5, Lpmsj/work/b/ab;->R:Z

    if-eqz v5, :cond_18

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/ab;->M()Z

    move-result v5

    if-eqz v5, :cond_15

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/ab;->ab()Z

    move-result v5

    if-nez v5, :cond_15

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->u:Lpmsj/work/main/c;

    move-object v5, v0

    const-string v6, "\u5bfc\u822a\u4e2d..."

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v7

    invoke-virtual {v7}, Lpmsj/work/b/ab;->e()I

    move-result v7

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v8

    invoke-virtual {v8}, Lpmsj/work/b/ab;->b()I

    move-result v8

    move-object v0, v5

    move-object/from16 v1, p1

    move-object v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/main/c;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;II)V

    :cond_15
    :goto_8
    invoke-super/range {p0 .. p3}, Lpmsj/work/d/c;->b(Ljavax/microedition/lcdui/Graphics;II)V

    sget-boolean v5, Lpmsj/work/main/f;->f:Z

    if-eqz v5, :cond_17

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/d/g;->G()Z

    move-result v5

    if-eqz v5, :cond_17

    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-eqz v5, :cond_16

    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v6, 0x1f

    invoke-virtual {v5, v6}, Lpmsj/work/b/ab;->f(B)I

    move-result v5

    sget-object v6, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v7, 0x20

    invoke-virtual {v6, v7}, Lpmsj/work/b/ab;->f(B)I

    move-result v6

    if-lt v5, v6, :cond_19

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v5, v0

    iget v5, v5, Lpmsj/work/d/b;->k:I

    :goto_9
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aG:Lpmsj/work/a/i;

    move-object v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v7, v0

    iget-short v7, v7, Lpmsj/work/d/b;->i:S

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v8, v0

    iget-short v8, v8, Lpmsj/work/d/b;->j:S

    add-int/lit8 v8, v8, 0x1

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aG:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v9, v0

    iget v9, v9, Lpmsj/work/d/b;->k:I

    move-object v0, v6

    move v1, v7

    move v2, v8

    move v3, v9

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aH:Lpmsj/work/a/i;

    move-object v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v7, v0

    iget-short v7, v7, Lpmsj/work/d/b;->i:S

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v8, v0

    iget-short v8, v8, Lpmsj/work/d/b;->j:S

    add-int/lit8 v8, v8, 0x1

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->aH:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    move-object v0, v6

    move v1, v7

    move v2, v8

    move v3, v5

    move-object/from16 v4, p1

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(IIILjavax/microedition/lcdui/Graphics;)V

    :cond_16
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/main/k;->ab:B

    move v6, v0

    move-object/from16 v0, p1

    move-object v1, v5

    move v2, v6

    invoke-static {v0, v1, v2}, Lpmsj/work/main/c;->a(Ljavax/microedition/lcdui/Graphics;Lpmsj/work/d/g;I)V

    :cond_17
    const/4 v5, -0x1

    move v0, v5

    move-object/from16 v1, p0

    iput-byte v0, v1, Lpmsj/work/main/k;->ab:B

    goto/16 :goto_7

    :cond_18
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v5

    iget-object v5, v5, Lpmsj/work/b/ab;->L:La/b/c;

    if-eqz v5, :cond_15

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->u:Lpmsj/work/main/c;

    move-object v5, v0

    const-string v6, "\u5bfb\u602a\u4e2d..."

    const/4 v7, 0x0

    const/4 v8, 0x0

    move-object v0, v5

    move-object/from16 v1, p1

    move-object v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/main/c;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;II)V

    goto/16 :goto_8

    :cond_19
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    move-object v7, v0

    iget v7, v7, Lpmsj/work/d/b;->k:I

    mul-int/2addr v5, v7

    int-to-long v7, v5

    int-to-long v5, v6

    div-long v5, v7, v5
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_0

    long-to-int v5, v5

    goto/16 :goto_9

    :cond_1a
    move v10, v5

    goto/16 :goto_5

    :cond_1b
    move v8, v5

    goto/16 :goto_0
.end method

.method public final b(I)Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 8

    const/16 v7, 0x3ff

    const/16 v5, 0x3e8

    const/4 v4, 0x2

    const/4 v6, 0x0

    const/4 v2, 0x1

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-le v0, v2, :cond_1

    move v1, v6

    :goto_0
    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v1, v0, :cond_1

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    invoke-virtual {v0}, Lpmsj/work/b/n;->p()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v3, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v3

    if-eqz v3, :cond_0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->a(Lpmsj/work/b/n;)V

    invoke-direct {p0}, Lpmsj/work/main/k;->ar()V

    iget-object v1, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->removeAllElements()V

    iget-object v1, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move v0, v2

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v1, 0x1

    move v1, v0

    goto :goto_0

    :cond_1
    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    if-eqz v0, :cond_2

    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-nez v0, :cond_4

    :cond_2
    move v0, v6

    :cond_3
    :goto_2
    if-eqz v0, :cond_17

    move v0, v2

    goto :goto_1

    :cond_4
    iget-object v0, p0, Lpmsj/work/main/k;->at:Ljava/util/Vector;

    invoke-virtual {v0, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/n;

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    if-eqz v1, :cond_5

    instance-of v0, v0, Lpmsj/work/b/v;

    if-nez v0, :cond_6

    :cond_5
    move v0, v6

    :goto_3
    if-eqz v0, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    const/4 v3, 0x0

    invoke-virtual {v1, v3}, Lpmsj/work/b/m;->a(Lpmsj/work/b/n;)V

    goto :goto_2

    :cond_6
    const-string v0, "\u4ea4\u6613"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_7

    sget-object v0, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v0}, Lpmsj/work/b/v;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/main/e;->a(I)V

    move v0, v2

    goto :goto_3

    :cond_7
    const-string v0, "\u52a0\u53cb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_8

    invoke-static {}, Lpmsj/work/main/i;->a()Lpmsj/work/main/i;

    sget-object v0, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v0}, Lpmsj/work/b/v;->u()I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, Lpmsj/work/main/i;->a(ILjava/lang/String;)V

    move v0, v2

    goto :goto_3

    :cond_8
    const-string v0, "\u67e5\u770b"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_9

    const/16 v0, 0x517

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->u()I

    move-result v1

    invoke-static {v0, v2, v1}, Lpmsj/work/main/w;->a(IBI)V

    const/16 v0, 0x441

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->u()I

    move-result v1

    invoke-static {v0, v4, v1}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto :goto_3

    :cond_9
    const-string v0, "\u79c1\u804a"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_a

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x15

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/w;

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/e/w;->g(Ljava/lang/String;)V

    move v0, v2

    goto :goto_3

    :cond_a
    const-string v0, "PK"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_b

    const/16 v0, 0x486

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v4, v1, v3}, Lpmsj/work/main/w;->a(IBII)V

    move v0, v2

    goto/16 :goto_3

    :cond_b
    const-string v0, "\u5207\u78cb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_c

    const/16 v0, 0x485

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v4, v1, v3}, Lpmsj/work/main/w;->a(IBII)V

    move v0, v2

    goto/16 :goto_3

    :cond_c
    const-string v0, "\u7ec4\u961f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_d

    sget-object v0, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v0}, Lpmsj/work/b/v;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->f(I)V

    move v0, v2

    goto/16 :goto_3

    :cond_d
    const-string v0, "\u6bd4\u6b66"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_e

    const/16 v0, 0x5ee

    const/4 v1, 0x7

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v3}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto/16 :goto_3

    :cond_e
    const-string v0, "\u89c2\u6218"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_f

    const/16 v0, 0x410

    const/4 v1, 0x5

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v3}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto/16 :goto_3

    :cond_f
    const-string v0, "\u6682\u79bb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_10

    const/16 v0, 0x12

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_3

    :cond_10
    const-string v0, "\u5f52\u961f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_11

    const/16 v0, 0x11

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_3

    :cond_11
    const-string v0, "\u4ea4\u961f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_12

    const/4 v0, 0x0

    const-string v1, "\u60a8\u786e\u5b9a\u63d0\u5347    "

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-result-object v0

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "    \u4e3a\u65b0\u7684\u961f\u957f\u5417\uff1f"

    invoke-static {v0, v1}, La/c/x;->a(Ljava/lang/StringBuffer;Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    const/16 v3, 0x2c

    invoke-virtual {v1, v0, v3, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    move v0, v2

    goto/16 :goto_3

    :cond_12
    const-string v0, "\u8d60\u9001"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_13

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/b/a;->e()Ljava/util/Vector;

    move-result-object v0

    sget-object v1, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v1}, Lpmsj/work/b/v;->p()Ljava/lang/String;

    move-result-object v1

    invoke-static {v0, v1, p0}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Ljava/lang/String;Lpmsj/work/d/c;)V

    move v0, v2

    goto/16 :goto_3

    :cond_13
    const-string v0, "\u62dc\u5e08"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_14

    const/16 v0, 0x43a

    const/4 v1, 0x4

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v3}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto/16 :goto_3

    :cond_14
    const-string v0, "\u6536\u5f92"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_15

    const/16 v0, 0x43a

    const/4 v1, 0x3

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v3}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto/16 :goto_3

    :cond_15
    const-string v0, "\u6218\u6597"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_16

    const/16 v0, 0x447

    const/4 v1, 0x3

    sget-object v3, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v3}, Lpmsj/work/b/v;->u()I

    move-result v3

    invoke-static {v0, v1, v3}, Lpmsj/work/main/w;->a(IBI)V

    move v0, v2

    goto/16 :goto_3

    :cond_16
    move v0, v6

    goto/16 :goto_3

    :cond_17
    const-string v0, "BattleTest"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1a

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "/battle2 11400 10"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, ""

    invoke-virtual {v0, v1, v4, v3}, Lpmsj/work/main/d;->a(Ljava/lang/StringBuffer;BLjava/lang/String;)Ljava/lang/StringBuffer;

    :cond_18
    :goto_4
    const-string v0, "\u4efb\u52a1"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_34

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->i()Lpmsj/work/e/ej;

    :cond_19
    :goto_5
    move v0, v6

    goto/16 :goto_1

    :cond_1a
    const-string v0, "awardEudemon"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1b

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "/awardEudemon 10100"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, ""

    invoke-virtual {v0, v1, v4, v3}, Lpmsj/work/main/d;->a(Ljava/lang/StringBuffer;BLjava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_4

    :cond_1b
    const-string v0, "ReloadAction"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1c

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "/reloadaction 0"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, ""

    invoke-virtual {v0, v1, v4, v3}, Lpmsj/work/main/d;->a(Ljava/lang/StringBuffer;BLjava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_4

    :cond_1c
    const-string v0, "ReloadScript"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1d

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "/reloadscript"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, ""

    invoke-virtual {v0, v1, v4, v3}, Lpmsj/work/main/d;->a(Ljava/lang/StringBuffer;BLjava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_4

    :cond_1d
    const-string v0, "ReloadQuest"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1e

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "/reloadquest"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v3, ""

    invoke-virtual {v0, v1, v4, v3}, Lpmsj/work/main/d;->a(Ljava/lang/StringBuffer;BLjava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_4

    :cond_1e
    const-string v0, "\u89d2\u8272\u4fe1\u606f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1f

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    goto/16 :goto_4

    :cond_1f
    const-string v0, "\u7269\u54c1\u80cc\u5305"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_20

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x5

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_20
    const-string v0, "\u90ae\u7bb1"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_21

    const-string v0, "\u67e5\u770b\u90ae\u7bb1"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_22

    :cond_21
    sput-boolean v6, Lpmsj/work/main/t;->v:Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25d

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_22
    sget-object v0, Lpmsj/work/a/c;->aJ:[Ljava/lang/String;

    aget-object v0, v0, v6

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_23

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->i()Lpmsj/work/e/ej;

    goto/16 :goto_4

    :cond_23
    const-string v0, "\u6392\u884c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_24

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-virtual {v0, v5}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_4

    :cond_24
    const-string v0, "\u961f\u4f0d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_27

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-nez v0, :cond_25

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->aa()Z

    move-result v0

    if-eqz v0, :cond_26

    :cond_25
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_26
    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->aa()Z

    move-result v0

    if-nez v0, :cond_18

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5b

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_27
    const-string v0, "\u4ed9\u6676\u5546\u5e97"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_28

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x263

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_28
    const-string v0, "\u804a\u5929"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_29

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x15

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_29
    const-string v0, "\u7cfb\u7edf\u8bbe\u7f6e"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2a

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5f

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_2a
    const-string v0, "\u5ba0\u7269\u5217\u8868"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2b

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x208

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_2b
    const-string v0, "\u5e2e\u6d3e"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2d

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->W()I

    move-result v0

    if-nez v0, :cond_2c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x132

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_2c
    const/16 v0, 0x453

    const/16 v1, 0xb

    invoke-static {v0, v1, v6}, Lpmsj/work/main/w;->a(ISI)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x13e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_2d
    const-string v0, "\u793e\u4ea4\u5173\u7cfb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2e

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->k()Lpmsj/work/e/ei;

    goto/16 :goto_4

    :cond_2e
    const-string v0, "\u67e5\u770b\u644a\u4f4d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_2f

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xcd

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_2f
    const-string v0, "\u5173\u95ed\u644a\u4f4d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_30

    const/16 v0, 0x6c3

    const/4 v1, 0x7

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_4

    :cond_30
    const-string v0, "\u644a\u4f4d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_31

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xd2

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_4

    :cond_31
    const-string v0, "\u64cd\u4f5c\u8fd4\u56de"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_32

    move v0, v2

    goto/16 :goto_1

    :cond_32
    const-string v0, "\u4e45\u6e38"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_18

    const-string v0, "\u6218\u6597"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_33

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v0, 0x7ed

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->h()I

    move-result v1

    invoke-static {v0, v2, v1}, Lpmsj/work/main/w;->a(IBI)V

    goto/16 :goto_4

    :cond_33
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->x()Lpmsj/work/b/i;

    move-result-object v0

    if-eqz v0, :cond_18

    const/16 v1, 0x9

    invoke-virtual {v0, v1}, Lpmsj/work/b/i;->j(B)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_18

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->am()V

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v0, 0x7eb

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->h()I

    move-result v1

    invoke-static {v0, v2, v1}, Lpmsj/work/main/w;->a(IBI)V

    goto/16 :goto_4

    :cond_34
    const-string v0, "\u526f\u672c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_35

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x18c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_35
    const-string v0, "\u795e\u70bc\u503c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_36

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x198

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_36
    const-string v0, "\u98d8\u6e3a\u52a9\u624b"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_37

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x1f5

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/h;

    invoke-virtual {p0, v6}, Lpmsj/work/e/h;->y(I)V

    goto/16 :goto_5

    :cond_37
    const-string v0, "\u6d3b\u52a8"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_38

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x142

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    goto/16 :goto_5

    :cond_38
    const-string v0, "\u6307\u5f15"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_39

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x142

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/4 v1, 0x5

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    goto/16 :goto_5

    :cond_39
    const-string v0, "\u6210\u5c31"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3a

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_3a
    const-string v0, "\u9886\u6210\u5c31\u5956"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3b

    sput-boolean v6, Lpmsj/work/main/t;->w:Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/f;

    invoke-virtual {p0}, Lpmsj/work/e/f;->i()V

    goto/16 :goto_5

    :cond_3b
    const-string v0, "\u4eba\u7269\u88c5\u5907"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x12

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/af;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {p0, v0, v1}, Lpmsj/work/e/af;->a(Lpmsj/work/b/v;Ljava/util/Vector;)V

    goto/16 :goto_5

    :cond_3c
    const-string v0, "\u4fee\u771f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3d

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14b

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_3d
    const-string v0, "\u4eba\u7269\u5c5e\u6027"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3e

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    goto/16 :goto_5

    :cond_3e
    const-string v0, "\u4eba\u7269\u6280\u80fd"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_3f

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xcb

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_3f
    const-string v0, "\u5750\u9a91"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_40

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x160

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_40
    const-string v0, "\u58f0\u671b"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_41

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x142

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/d/c;->y(I)V

    goto/16 :goto_5

    :cond_41
    const-string v0, "\u798f\u7f18"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_42

    const-string v0, "\u798f\u7f18\u7cfb\u7edf"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_43

    :cond_42
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x152

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_43
    const-string v0, "\u5468\u56f4\u73a9\u5bb6"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_44

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xc

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->j(I)V

    goto/16 :goto_5

    :cond_44
    const-string v0, "\u6253\u9020\u88c5\u5907"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_45

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/16 v1, 0x898

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_45
    const-string v0, "4\u4ed3\u5e93"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_46

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v0, 0x43d

    invoke-static {v0, v4}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_46
    const-string v0, "\u516c\u544a"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_47

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x181

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/16 v1, 0x960

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_47
    const-string v0, "\u5ba0\u7269\u5408\u6210"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_48

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x69

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ck;

    invoke-virtual {p0, v6}, Lpmsj/work/e/ck;->y(I)V

    goto/16 :goto_5

    :cond_48
    const-string v0, "\u5ba0\u7269\u4ed3\u5e93"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_49

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/16 v1, 0x960

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_49
    const-string v0, "\u968f\u8eab\u4fee\u70bc"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4a

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v0, 0x43d

    invoke-static {v0, v2}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_4a
    const-string v0, "\u8054\u7cfbGM"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4b

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "*3\u5411GM\u7559\u8a00\uff08\u6b21\u65e5\u5904\u7406\u53cd\u9988\uff09"

    const/16 v4, 0xff

    const-string v5, ""

    const-string v7, ""

    move-object v3, p0

    invoke-virtual/range {v0 .. v7}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_4b
    const-string v0, "\u5ba0\u7269\u70bc\u5316"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x69

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ck;

    invoke-virtual {p0, v2}, Lpmsj/work/e/ck;->y(I)V

    goto/16 :goto_5

    :cond_4c
    const-string v0, "\u4e94\u884c\u953b\u9020"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4d

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x67

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ah;

    invoke-virtual {p0, v2}, Lpmsj/work/e/ah;->y(I)V

    goto/16 :goto_5

    :cond_4d
    const-string v0, "\u6e38\u620f\u5e2e\u52a9"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4e

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xc

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_4e
    const-string v0, "\u521b\u5efa\u961f\u4f0d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_4f

    invoke-static {}, Lpmsj/work/b/aa;->e()V

    move v0, v2

    goto/16 :goto_1

    :cond_4f
    const-string v0, "\u7533\u8bf7\u52a0\u5165"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_50

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Y()Z

    move-result v0

    if-nez v0, :cond_19

    const/16 v0, 0x32

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    invoke-static {v7, v0, v1}, Lpmsj/work/main/w;->a(ISI)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_50
    const-string v0, "\u81ea\u52a8\u52a0\u5165"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_53

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Y()Z

    move-result v0

    if-nez v0, :cond_19

    sget-boolean v0, Lpmsj/work/b/aa;->g:Z

    if-nez v0, :cond_51

    move v0, v2

    :goto_6
    sput-boolean v0, Lpmsj/work/b/aa;->g:Z

    if-eqz v0, :cond_52

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u60a8\u5df2\u5f00\u542f\u4e86\u961f\u4f0d\u7684\u81ea\u52a8\u52a0\u5165\u529f\u80fd\uff01"

    invoke-virtual {v0, v1, v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    const/16 v0, 0xf

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    goto/16 :goto_5

    :cond_51
    move v0, v6

    goto :goto_6

    :cond_52
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u60a8\u5df2\u5173\u95ed\u4e86\u961f\u4f0d\u7684\u81ea\u52a8\u52a0\u5165\u529f\u80fd\uff01"

    invoke-virtual {v0, v1, v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    const/16 v0, 0x10

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    goto/16 :goto_5

    :cond_53
    const-string v0, "\u81ea\u52a8\u62d2\u7edd"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_56

    sget-boolean v0, Lpmsj/work/b/aa;->f:Z

    if-nez v0, :cond_54

    move v0, v2

    :goto_7
    sput-boolean v0, Lpmsj/work/b/aa;->f:Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    sget-boolean v1, Lpmsj/work/b/aa;->f:Z

    if-eqz v1, :cond_55

    const-string v1, "\u60a8\u5df2\u5f00\u542f\u4e86\u961f\u4f0d\u7684\u62d2\u7ec4\u529f\u80fd"

    :goto_8
    invoke-virtual {v0, v1, v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_5

    :cond_54
    move v0, v6

    goto :goto_7

    :cond_55
    const-string v1, "\u60a8\u5df2\u5173\u95ed\u4e86\u961f\u4f0d\u7684\u62d2\u7ec4\u529f\u80fd"

    goto :goto_8

    :cond_56
    const-string v0, "\u7533\u8bf7\u5217\u8868"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_57

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x51

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_57
    const-string v0, "\u961f\u4f0d\u4fe1\u606f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_58

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x131

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_58
    const-string v0, "\u9080\u8bf7\u52a0\u5165"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_59

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->j(I)V

    goto/16 :goto_5

    :cond_59
    const-string v0, "\u81ea\u52a8\u9080\u8bf7"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_5c

    sget-boolean v0, Lpmsj/work/b/aa;->d:Z

    if-nez v0, :cond_5a

    move v0, v2

    :goto_9
    sput-boolean v0, Lpmsj/work/b/aa;->d:Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    sget-boolean v1, Lpmsj/work/b/aa;->d:Z

    if-eqz v1, :cond_5b

    const-string v1, "\u60a8\u5df2\u5f00\u542f\u4e86\u961f\u4f0d\u7684\u81ea\u52a8\u9080\u8bf7\u529f\u80fd\uff01"

    :goto_a
    invoke-virtual {v0, v1, v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_5

    :cond_5a
    move v0, v6

    goto :goto_9

    :cond_5b
    const-string v1, "\u60a8\u5df2\u5173\u95ed\u4e86\u961f\u4f0d\u7684\u81ea\u52a8\u9080\u8bf7\u529f\u80fd\uff01"

    goto :goto_a

    :cond_5c
    const-string v0, "\u6682\u79bb\u961f\u4f0d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_5d

    const/16 v0, 0x12

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_1

    :cond_5d
    const-string v0, "\u5f52\u961f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_5e

    const/16 v0, 0x11

    invoke-static {v7, v0}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_1

    :cond_5e
    const-string v0, "\u79bb\u5f00\u961f\u4f0d"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_60

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-eqz v0, :cond_5f

    sget-object v0, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-le v0, v2, :cond_5f

    const-string v0, "\u662f\u5426\u786e\u8ba4\u79bb\u5f00\u961f\u4f0d\uff1f"

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v3, 0xe

    invoke-virtual {v1, v0, v3, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    :goto_b
    move v0, v2

    goto/16 :goto_1

    :cond_5f
    invoke-static {}, Lpmsj/work/b/aa;->d()V

    goto :goto_b

    :cond_60
    const-string v0, "\u4ed9\u77f3\u5546\u5e97"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_61

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/16 v1, 0x834

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_61
    const-string v0, "\u5546\u5e97\u4ed9\u6676"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_62

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    const/16 v1, 0x7d0

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_62
    const-string v0, "\u8d26\u53f7\u5145\u503c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_63

    invoke-static {}, Lpmsj/work/main/MyMidlet;->c()V

    goto/16 :goto_5

    :cond_63
    const-string v0, "\u9886\u5956"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_64

    const/16 v0, 0x5fe

    invoke-static {v0, v6}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_64
    const-string v0, "\u8d26\u53f7\u793c\u5305"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_65

    const/16 v0, 0x5fe

    invoke-static {v0, v2}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_65
    const-string v0, "\u9886\u4ed9\u6676"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_66

    const/16 v0, 0x5fe

    invoke-static {v0, v4}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_66
    const-string v0, "\u7d2f\u8ba1\u793c\u5305"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_67

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x177

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_67
    const-string v0, "\u8bbe\u7f6e"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_68

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x17

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_68
    const-string v0, "\u9000\u51fa\u6e38\u620f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_69

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x18b

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/cw;

    invoke-static {p0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    const/16 v0, 0x41e

    const/16 v1, 0x8

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    move v0, v2

    goto/16 :goto_1

    :cond_69
    const-string v0, "\u81ea\u52a8\u5bfb\u8def"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-nez v0, :cond_6a

    const-string v0, "\u5468\u56f4NPC"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6b

    :cond_6a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x12c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_6b
    const-string v0, "\u5f53\u524d\u5730\u56fe"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6c

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x2e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_6c
    const-string v0, "\u4e16\u754c\u5730\u56fe"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6d

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x2d

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bn;

    invoke-virtual {p0, v5}, Lpmsj/work/d/c;->y(I)V

    invoke-static {p0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_6d
    const-string v0, "\u5e08\u5f92"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6e

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25f

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_6e
    const-string v0, "\u73a9\u5bb6\u4ea4\u6613"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_6f

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x9

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->j(I)V

    goto/16 :goto_5

    :cond_6f
    const-string v0, "\u6dfb\u52a0\u597d\u53cb"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_70

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xb

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->j(I)V

    goto/16 :goto_5

    :cond_70
    const-string v0, "\u597d\u53cb\u5217\u8868"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_71

    invoke-static {}, Lpmsj/work/main/c;->a()Lpmsj/work/main/c;

    sget-object v0, Lpmsj/work/b/f;->g:Ljava/util/Vector;

    invoke-static {v0}, Lpmsj/work/main/c;->a(Ljava/util/Vector;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x262

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_71
    const-string v0, "\u67e5\u8be2\u73a9\u5bb6"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_72

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xa

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->j(I)V

    goto/16 :goto_5

    :cond_72
    const-string v0, "\u9ed1\u540d\u5355"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_73

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x12f

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto/16 :goto_5

    :cond_73
    const-string v0, "\u4ec7\u4eba\u5217\u8868"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_74

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x261

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    const/16 v0, 0x3fb

    const/16 v1, 0x1c

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_5

    :cond_74
    const-string v0, "\u6392\u884c\u699c"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_75

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x154

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-virtual {v0, v5}, Lpmsj/work/d/c;->y(I)V

    invoke-static {v0}, Lpmsj/work/main/k;->b(Lpmsj/work/d/c;)V

    goto/16 :goto_5

    :cond_75
    const-string v0, "\u81ea\u52a8\u8865\u836f"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_76

    const/16 v0, 0x3f2

    const/16 v1, 0x3e

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_1

    :cond_76
    const-string v0, "\u81ea\u52a8\u6302\u673a"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_77

    const/16 v0, 0x3f2

    const/16 v1, 0x118

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IS)V

    move v0, v2

    goto/16 :goto_1

    :cond_77
    const-string v0, "\u89d2\u8272\u72b6\u6001"

    invoke-virtual {p1, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_19

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x141

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move v0, v2

    goto/16 :goto_1
.end method

.method public final b_()Lpmsj/work/d/l;
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    return-object v0
.end method

.method public final b_(I)V
    .locals 4

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0, p1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, ""

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    const/4 v1, 0x4

    invoke-virtual {v0}, Ljava/lang/String;->length()I

    move-result v2

    sub-int/2addr v1, v2

    mul-int/lit8 v1, v1, 0x5

    div-int/lit8 v1, v1, 0x2

    iget-object v2, p0, Lpmsj/work/main/k;->an:Lpmsj/work/d/d;

    invoke-virtual {v2, v0}, Lpmsj/work/d/d;->b(Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/main/k;->an:Lpmsj/work/d/d;

    iget-object v2, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    iget-short v2, v2, Lpmsj/work/d/b;->i:S

    add-int/2addr v1, v2

    iget-object v2, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    invoke-virtual {v2}, Lpmsj/work/d/a;->E()I

    move-result v2

    const/4 v3, 0x7

    sub-int/2addr v2, v3

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/d;->f(II)V

    iget-object v0, p0, Lpmsj/work/main/k;->an:Lpmsj/work/d/d;

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->f(Lpmsj/work/d/b;)V

    return-void
.end method

.method protected final c()V
    .locals 10

    const v9, 0x20d343

    const/16 v8, 0x135

    const/4 v7, 0x3

    const/4 v6, 0x1

    const/4 v5, 0x0

    const/16 v0, 0xbc0

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/l;

    iput-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    const/16 v1, 0x100

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->l(I)V

    invoke-virtual {p0}, Lpmsj/work/main/k;->p()V

    const/16 v0, 0x2008

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->q(I)V

    const v0, 0x5fac30

    invoke-static {v0}, La/a/f;->a(I)La/a/e;

    move-result-object v0

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/4 v2, 0x6

    invoke-virtual {v1, v2}, Lpmsj/work/b/ab;->f(B)I

    move-result v1

    new-instance v2, Lpmsj/work/a/i;

    add-int/lit16 v1, v1, 0x190

    mul-int/lit16 v1, v1, 0x2710

    invoke-direct {v2, v1}, Lpmsj/work/a/i;-><init>(I)V

    iput-object v2, p0, Lpmsj/work/main/k;->af:Lpmsj/work/a/i;

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/k;->ag:Lpmsj/work/d/d;

    invoke-virtual {v0}, La/a/e;->a()I

    move-result v2

    const/16 v3, 0x39

    sub-int/2addr v2, v3

    invoke-virtual {v0}, La/a/e;->b()I

    move-result v3

    const/16 v4, 0x8

    sub-int/2addr v3, v4

    invoke-virtual {v1, v2, v3}, Lpmsj/work/d/d;->f(II)V

    iget-object v1, p0, Lpmsj/work/main/k;->ah:Lpmsj/work/d/d;

    invoke-virtual {v0}, La/a/e;->a()I

    move-result v2

    const/16 v3, 0x28

    sub-int/2addr v2, v3

    invoke-virtual {v0}, La/a/e;->b()I

    move-result v0

    const/16 v3, 0xa

    sub-int/2addr v0, v3

    invoke-virtual {v1, v2, v0}, Lpmsj/work/d/d;->f(II)V

    :cond_0
    const/16 v0, 0xbc5

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    new-instance v1, Lpmsj/work/a/i;

    const v0, 0x20d4d3

    invoke-direct {v1, v0, v5}, Lpmsj/work/a/i;-><init>(II)V

    new-instance v0, Lpmsj/work/a/i;

    invoke-direct {v0, v9, v5}, Lpmsj/work/a/i;-><init>(II)V

    iget-object v2, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    invoke-virtual {v2, v1, v0}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    iput-short v5, v0, Lpmsj/work/d/b;->i:S

    iget-object v0, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    sget-short v2, Lpmsj/work/main/t;->d:S

    invoke-virtual {v1}, Lpmsj/work/a/i;->b()I

    move-result v3

    sub-int/2addr v2, v3

    int-to-short v2, v2

    iput-short v2, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/main/k;->Z:Lpmsj/work/d/a;

    invoke-virtual {v0, v5}, Lpmsj/work/d/a;->c(I)V

    const/16 v0, 0xbc6

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    new-instance v2, Lpmsj/work/a/i;

    const v3, 0x20d4d3

    invoke-direct {v2, v3, v5}, Lpmsj/work/a/i;-><init>(II)V

    new-instance v3, Lpmsj/work/a/i;

    invoke-direct {v3, v9, v5}, Lpmsj/work/a/i;-><init>(II)V

    invoke-virtual {v0, v2, v3}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    sget-short v2, Lpmsj/work/main/t;->c:S

    iget-object v3, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    iget v3, v3, Lpmsj/work/d/b;->k:I

    sub-int/2addr v2, v3

    int-to-short v2, v2

    iput-short v2, v0, Lpmsj/work/d/b;->i:S

    iget-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    sget-short v2, Lpmsj/work/main/t;->d:S

    invoke-virtual {v1}, Lpmsj/work/a/i;->b()I

    move-result v1

    sub-int v1, v2, v1

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/main/k;->aa:Lpmsj/work/d/a;

    invoke-virtual {v0, v5}, Lpmsj/work/d/a;->c(I)V

    const-string v0, "\u83dc\u5355"

    const-string v1, "\u64cd\u4f5c"

    invoke-virtual {p0, v0, v1}, Lpmsj/work/main/k;->a(Ljava/lang/String;Ljava/lang/String;)V

    const/16 v0, 0xbbd

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/g;

    iput-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    const/high16 v1, 0x180000

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->l(I)V

    const/16 v0, 0xbc2

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    const/high16 v1, 0x800000

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->l(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    sget v1, Lpmsj/work/a/c;->E:I

    iput v1, v0, Lpmsj/work/d/a;->m:I

    const/16 v0, 0xbc1

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/main/k;->Y:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/main/k;->Y:Lpmsj/work/d/a;

    const/high16 v1, 0x800000

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->l(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    sget-short v1, Lpmsj/work/main/t;->c:S

    iget-object v2, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    const/16 v2, 0xf

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->f(II)V

    iget-object v0, p0, Lpmsj/work/main/k;->Y:Lpmsj/work/d/a;

    sget-short v1, Lpmsj/work/main/t;->c:S

    iget-object v2, p0, Lpmsj/work/main/k;->Y:Lpmsj/work/d/a;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    iget-object v2, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    iget-short v2, v2, Lpmsj/work/d/b;->j:S

    add-int/lit8 v2, v2, 0x12

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->f(II)V

    const/16 v0, 0xbc7

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    iput-object v0, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    iget-object v0, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    new-instance v1, Lpmsj/work/a/i;

    const v2, 0x240dcc

    invoke-direct {v1, v2}, Lpmsj/work/a/i;-><init>(I)V

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->b(Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    new-instance v1, Lpmsj/work/a/i;

    const v2, 0x3cc458

    const/16 v3, 0xc

    invoke-direct {v1, v2, v3}, Lpmsj/work/a/i;-><init>(II)V

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->c(Lpmsj/work/a/i;)V

    iget-object v0, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    sget-short v1, Lpmsj/work/main/t;->c:S

    iget-object v2, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v2

    sub-int/2addr v1, v7

    invoke-virtual {v0, v1, v7}, Lpmsj/work/d/a;->f(II)V

    new-instance v0, Lpmsj/work/d/a;

    const-string v1, ""

    invoke-direct {v0, v1, v5, v5}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;II)V

    const-string v1, "#"

    invoke-virtual {v0, v1, v6, v6}, Lpmsj/work/d/a;->a(Ljava/lang/String;II)V

    iget-object v1, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    iget-short v1, v1, Lpmsj/work/d/b;->i:S

    iget-object v2, p0, Lpmsj/work/main/k;->am:Lpmsj/work/d/a;

    iget-short v2, v2, Lpmsj/work/d/b;->j:S

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/a;->f(II)V

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->f(Lpmsj/work/d/b;)V

    iget-object v0, p0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    sget-short v1, Lpmsj/work/main/t;->c:S

    const/16 v2, 0x23

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    add-int/lit8 v1, v1, 0xa

    invoke-virtual {v0, v1, v7}, Lpmsj/work/d/d;->f(II)V

    sget-boolean v0, Lpmsj/work/main/f;->g:Z

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/main/k;->ai:Lpmsj/work/d/d;

    invoke-direct {p0}, Lpmsj/work/main/k;->ap()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/d;->b(Ljava/lang/String;)V

    :cond_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->e(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/bs;

    iput-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0, v8}, Lpmsj/work/e/bs;->p(I)Z

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    const/4 v1, -0x1

    invoke-virtual {v0, v1}, Lpmsj/work/e/bs;->x(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0, v6}, Lpmsj/work/e/bs;->q(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->f(Lpmsj/work/d/b;)V

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0, v5}, Lpmsj/work/e/bs;->a(Z)V

    return-void
.end method

.method protected final c(I)Z
    .locals 2

    invoke-static {p1}, Lpmsj/work/main/k;->C(I)V

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x4

    aget-short v0, v0, v1

    if-eq v0, p1, :cond_0

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x5

    aget-short v0, v0, v1

    if-eq v0, p1, :cond_0

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x2

    aget-short v0, v0, v1

    if-eq v0, p1, :cond_0

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x3

    aget-short v0, v0, v1

    if-ne v0, p1, :cond_1

    :cond_0
    sget-object v0, Lpmsj/work/main/t;->x:La/c/q;

    invoke-virtual {v0}, La/c/q;->g()V

    :cond_1
    const/4 v0, 0x1

    iput-boolean v0, p0, Lpmsj/work/main/k;->as:Z

    invoke-virtual {p0, p1}, Lpmsj/work/main/k;->t(I)Z

    move-result v0

    return v0
.end method

.method public final c_(I)V
    .locals 9

    const/4 v8, 0x3

    const/4 v7, 0x2

    const/4 v5, 0x0

    const/4 v6, 0x1

    sparse-switch p1, :sswitch_data_0

    :goto_0
    return-void

    :sswitch_0
    const/16 v0, 0x3ff

    const/16 v1, 0x14

    sget-object v2, Lpmsj/work/b/f;->d:Lpmsj/work/b/v;

    invoke-virtual {v2}, Lpmsj/work/b/v;->u()I

    move-result v2

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :sswitch_1
    const/16 v0, 0x486

    const/4 v1, 0x6

    sget-object v2, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v2}, Lpmsj/work/b/ab;->u()I

    move-result v2

    sget v3, Lpmsj/work/main/e;->d:I

    invoke-static {v0, v1, v2, v3}, Lpmsj/work/main/w;->a(IBII)V

    goto :goto_0

    :sswitch_2
    invoke-static {}, Lpmsj/work/b/aa;->d()V

    goto :goto_0

    :sswitch_3
    sget-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    aget-object v0, v0, v5

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    sget-object v1, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    aget-object v1, v1, v6

    const/16 v2, 0x3fb

    new-instance v3, La/c/h;

    const/16 v4, 0xb

    invoke-direct {v3, v4}, La/c/h;-><init>(B)V

    new-instance v4, La/c/m;

    invoke-direct {v4, v0}, La/c/m;-><init>(I)V

    new-instance v0, La/c/p;

    invoke-direct {v0, v1}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static {v2, v3, v4, v0}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;)V

    goto :goto_0

    :sswitch_4
    const/16 v0, 0x420

    sget v1, Lpmsj/work/b/f;->e:I

    invoke-static {v0, v7, v1}, Lpmsj/work/main/w;->a(IBI)V

    goto :goto_0

    :sswitch_5
    const/16 v0, 0x453

    const/16 v1, 0x1e

    sget v2, Lpmsj/work/b/f;->f:I

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :sswitch_6
    const/16 v0, 0x419

    invoke-static {v0, v6, v6}, Lpmsj/work/main/w;->a(IBB)V

    goto :goto_0

    :sswitch_7
    const/16 v0, 0x406

    invoke-static {v0, v8}, Lpmsj/work/main/w;->a(IB)V

    goto :goto_0

    :sswitch_8
    const/16 v0, 0x5e5

    new-instance v1, La/c/h;

    iget-object v2, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-byte v2, v2, Lpmsj/work/main/l;->a:B

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/h;

    invoke-direct {v2, v6}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    iget-object v4, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v4, v4, Lpmsj/work/main/l;->b:[I

    aget v4, v4, v5

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    iget-object v5, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v5, v5, Lpmsj/work/main/l;->b:[I

    aget v5, v5, v6

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    iget-object v6, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v6, v6, Lpmsj/work/main/l;->b:[I

    aget v6, v6, v7

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    iget-object v7, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v7, v7, Lpmsj/work/main/l;->b:[I

    aget v7, v7, v8

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v6}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto/16 :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x2 -> :sswitch_3
        0x3 -> :sswitch_4
        0xe -> :sswitch_2
        0x19 -> :sswitch_5
        0x1f -> :sswitch_1
        0x23 -> :sswitch_6
        0x2b -> :sswitch_7
        0x2c -> :sswitch_0
        0x63 -> :sswitch_8
    .end sparse-switch
.end method

.method protected final e()V
    .locals 4

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/main/k;->aj:Lpmsj/work/d/d;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/main/k;->ae:La/c/q;

    invoke-virtual {v0}, La/c/q;->h()Z

    move-result v0

    if-eqz v0, :cond_7

    iget-object v0, p0, Lpmsj/work/main/k;->ae:La/c/q;

    invoke-virtual {v0}, La/c/q;->i()Z

    move-result v0

    if-nez v0, :cond_7

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->q()I

    move-result v0

    iget v1, p0, Lpmsj/work/main/k;->ac:I

    if-ne v0, v1, :cond_7

    iget-object v0, p0, Lpmsj/work/main/k;->ae:La/c/q;

    invoke-virtual {v0}, La/c/q;->l()I

    move-result v0

    div-int/lit16 v0, v0, 0x3e8

    if-lez v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/k;->V:Lpmsj/work/d/g;

    invoke-virtual {v1}, Lpmsj/work/d/g;->c()V

    iget-object v1, p0, Lpmsj/work/main/k;->aj:Lpmsj/work/d/d;

    const/high16 v2, 0x400000

    invoke-virtual {v1, v2}, Lpmsj/work/d/d;->l(I)V

    iget-object v1, p0, Lpmsj/work/main/k;->aj:Lpmsj/work/d/d;

    invoke-virtual {v1, v0}, Lpmsj/work/d/d;->a(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->V:Lpmsj/work/d/g;

    iget-object v1, p0, Lpmsj/work/main/k;->aj:Lpmsj/work/d/d;

    invoke-virtual {v0, v1, v3}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    :cond_0
    :goto_0
    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0}, Lpmsj/work/e/bs;->G()Z

    move-result v0

    if-eqz v0, :cond_1

    iget-object v0, p0, Lpmsj/work/main/k;->ao:Lpmsj/work/e/bs;

    invoke-virtual {v0}, Lpmsj/work/e/bs;->i()V

    :cond_1
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    if-eqz v0, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->u()Z

    move-result v1

    if-nez v1, :cond_3

    iget-object v1, v0, Lpmsj/work/b/ab;->L:La/b/c;

    if-eqz v1, :cond_2

    invoke-virtual {v0}, Lpmsj/work/b/ab;->al()V

    :cond_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->A()V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->y()V

    iget-boolean v1, p0, Lpmsj/work/main/k;->as:Z

    if-nez v1, :cond_8

    invoke-static {v3}, Lpmsj/work/main/k;->C(I)V

    :goto_1
    invoke-virtual {v0}, Lpmsj/work/b/ab;->ak()V

    :cond_3
    sget-boolean v0, Lpmsj/work/b/aa;->g:Z

    if-eqz v0, :cond_4

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Y()Z

    move-result v0

    if-nez v0, :cond_4

    invoke-static {}, Lpmsj/work/b/aa;->f()V

    :cond_4
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-eqz v0, :cond_5

    sget-boolean v0, Lpmsj/work/b/aa;->d:Z

    if-eqz v0, :cond_5

    sget-object v0, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    const/4 v1, 0x5

    if-ge v0, v1, :cond_5

    invoke-static {}, Lpmsj/work/b/aa;->g()V

    :cond_5
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iget-wide v2, p0, Lpmsj/work/main/k;->aJ:J

    sub-long/2addr v0, v2

    const-wide/16 v2, 0x1f40

    cmp-long v2, v0, v2

    if-lez v2, :cond_9

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iput-wide v0, p0, Lpmsj/work/main/k;->aJ:J

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->r()Z

    move-result v0

    if-eqz v0, :cond_6

    invoke-direct {p0}, Lpmsj/work/main/k;->at()V

    :cond_6
    :goto_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->n()V

    return-void

    :cond_7
    iget-object v0, p0, Lpmsj/work/main/k;->ae:La/c/q;

    invoke-virtual {v0}, La/c/q;->g()V

    iget-object v0, p0, Lpmsj/work/main/k;->V:Lpmsj/work/d/g;

    invoke-virtual {v0, v3}, Lpmsj/work/d/g;->a(Z)V

    iput v3, p0, Lpmsj/work/main/k;->ac:I

    goto/16 :goto_0

    :cond_8
    iput-boolean v3, p0, Lpmsj/work/main/k;->as:Z

    goto :goto_1

    :cond_9
    const-wide/16 v2, 0xbb8

    cmp-long v0, v0, v2

    if-lez v0, :cond_6

    invoke-virtual {p0}, Lpmsj/work/main/k;->p()V

    goto :goto_2
.end method

.method protected final f()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method

.method protected final g()V
    .locals 7

    const/16 v3, 0x8

    const/4 v2, 0x0

    const-string v6, "\u5468\u56f4\u73a9\u5bb6"

    const-string v5, "\u5468\u56f4NPC"

    const-string v4, "\u5173\u95ed\u644a\u4f4d"

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->L:La/b/c;

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    const/4 v1, 0x0

    iput-object v1, v0, Lpmsj/work/b/ab;->L:La/b/c;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iput v2, v0, Lpmsj/work/b/ab;->T:I

    :goto_0
    return-void

    :cond_0
    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ab()Z

    move-result v0

    if-nez v0, :cond_1

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0}, Lpmsj/work/b/ab;->M()Z

    move-result v0

    if-eqz v0, :cond_1

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ah()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iput v2, v0, Lpmsj/work/b/ab;->T:I

    goto :goto_0

    :cond_1
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->g()Lpmsj/work/b/n;

    move-result-object v0

    if-nez v0, :cond_9

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/util/Vector;

    invoke-direct {v1}, Ljava/util/Vector;-><init>()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->f()Z

    move-result v2

    if-eqz v2, :cond_5

    sget-boolean v2, Lpmsj/work/main/t;->w:Z

    if-eqz v2, :cond_2

    const-string v2, "\u9886\u6210\u5c31\u5956"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_2
    sget-boolean v2, Lpmsj/work/main/t;->v:Z

    if-eqz v2, :cond_3

    const-string v2, "\u67e5\u770b\u90ae\u7bb1"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_3
    sget-object v2, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v2, v3}, Lpmsj/work/b/ab;->a(I)Z

    move-result v2

    if-eqz v2, :cond_4

    const-string v2, "\u67e5\u770b\u644a\u4f4d"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5173\u95ed\u644a\u4f4d"

    invoke-virtual {v1, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_4
    const-string v2, "\u81ea\u52a8\u6302\u673a"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u89d2\u8272\u72b6\u6001"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5468\u56f4NPC"

    invoke-virtual {v1, v5}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5468\u56f4\u73a9\u5bb6"

    invoke-virtual {v1, v6}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u81ea\u52a8\u8865\u836f"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u798f\u7f18\u7cfb\u7edf"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u64cd\u4f5c\u8fd4\u56de"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "BattleTest"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "awardEudemon"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "ReloadAction"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "ReloadScript"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "ReloadQuest"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :goto_1
    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a(Ljava/util/Vector;Lpmsj/work/d/c;)V

    goto/16 :goto_0

    :cond_5
    sget-boolean v2, Lpmsj/work/main/t;->w:Z

    if-eqz v2, :cond_6

    const-string v2, "\u9886\u6210\u5c31\u5956"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_6
    sget-boolean v2, Lpmsj/work/main/t;->v:Z

    if-eqz v2, :cond_7

    const-string v2, "\u67e5\u770b\u90ae\u7bb1"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_7
    sget-object v2, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v2, v3}, Lpmsj/work/b/ab;->a(I)Z

    move-result v2

    if-eqz v2, :cond_8

    const-string v2, "\u67e5\u770b\u644a\u4f4d"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5173\u95ed\u644a\u4f4d"

    invoke-virtual {v1, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_8
    const-string v2, "\u81ea\u52a8\u6302\u673a"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u89d2\u8272\u72b6\u6001"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5468\u56f4NPC"

    invoke-virtual {v1, v5}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u5468\u56f4\u73a9\u5bb6"

    invoke-virtual {v1, v6}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u81ea\u52a8\u8865\u836f"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u798f\u7f18\u7cfb\u7edf"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const-string v2, "\u64cd\u4f5c\u8fd4\u56de"

    invoke-virtual {v1, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_1

    :cond_9
    invoke-direct {p0}, Lpmsj/work/main/k;->ar()V

    goto/16 :goto_0
.end method

.method public final g(I)V
    .locals 9

    const/16 v0, 0x5e5

    const/4 v7, 0x2

    const/4 v8, 0x3

    const/4 v6, 0x1

    const/4 v5, 0x0

    sparse-switch p1, :sswitch_data_0

    :goto_0
    return-void

    :sswitch_0
    sget-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    aget-object v0, v0, v5

    invoke-static {v0}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    sget-object v1, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    aget-object v1, v1, v6

    const/16 v2, 0x3fb

    new-instance v3, La/c/h;

    const/16 v4, 0x14

    invoke-direct {v3, v4}, La/c/h;-><init>(B)V

    new-instance v4, La/c/m;

    invoke-direct {v4, v0}, La/c/m;-><init>(I)V

    new-instance v0, La/c/p;

    invoke-direct {v0, v1}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static {v2, v3, v4, v0}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;)V

    goto :goto_0

    :sswitch_1
    const/16 v0, 0x420

    sget v1, Lpmsj/work/b/f;->e:I

    invoke-static {v0, v8, v1}, Lpmsj/work/main/w;->a(IBI)V

    goto :goto_0

    :sswitch_2
    const/16 v0, 0x453

    const/16 v1, 0x19

    sget v2, Lpmsj/work/b/f;->f:I

    invoke-static {v0, v1, v2}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :sswitch_3
    const/16 v0, 0x419

    invoke-static {v0, v6, v5}, Lpmsj/work/main/w;->a(IBB)V

    goto :goto_0

    :sswitch_4
    const/16 v0, 0x406

    const/4 v1, 0x4

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    goto :goto_0

    :sswitch_5
    new-instance v1, La/c/h;

    iget-object v2, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-byte v2, v2, Lpmsj/work/main/l;->a:B

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/h;

    invoke-direct {v2, v5}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    iget-object v4, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v4, v4, Lpmsj/work/main/l;->b:[I

    aget v4, v4, v5

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    iget-object v5, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v5, v5, Lpmsj/work/main/l;->b:[I

    aget v5, v5, v6

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    iget-object v6, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v6, v6, Lpmsj/work/main/l;->b:[I

    aget v6, v6, v7

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    iget-object v7, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v7, v7, Lpmsj/work/main/l;->b:[I

    aget v7, v7, v8

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v6}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto :goto_0

    :sswitch_6
    new-instance v1, La/c/h;

    iget-object v2, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-byte v2, v2, Lpmsj/work/main/l;->a:B

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/h;

    invoke-direct {v2, v5}, La/c/h;-><init>(B)V

    new-instance v3, La/c/m;

    iget-object v4, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v4, v4, Lpmsj/work/main/l;->b:[I

    aget v4, v4, v5

    invoke-direct {v3, v4}, La/c/m;-><init>(I)V

    new-instance v4, La/c/m;

    iget-object v5, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v5, v5, Lpmsj/work/main/l;->b:[I

    aget v5, v5, v6

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/m;

    iget-object v6, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v6, v6, Lpmsj/work/main/l;->b:[I

    aget v6, v6, v7

    invoke-direct {v5, v6}, La/c/m;-><init>(I)V

    new-instance v6, La/c/m;

    iget-object v7, p0, Lpmsj/work/main/k;->e:Lpmsj/work/main/l;

    iget-object v7, v7, Lpmsj/work/main/l;->b:[I

    aget v7, v7, v8

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    new-instance v7, La/c/p;

    const-string v8, ""

    invoke-direct {v7, v8}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static/range {v0 .. v7}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto/16 :goto_0

    :sswitch_data_0
    .sparse-switch
        0x2 -> :sswitch_0
        0x3 -> :sswitch_1
        0x19 -> :sswitch_2
        0x23 -> :sswitch_3
        0x2b -> :sswitch_4
        0x63 -> :sswitch_5
        0x64 -> :sswitch_6
    .end sparse-switch
.end method

.method public final h()V
    .locals 2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x166

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    const/16 v0, 0x40f

    const/4 v1, 0x1

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    return-void
.end method

.method public final h(I)V
    .locals 0

    return-void
.end method

.method public final i()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/main/k;->X:Lpmsj/work/d/a;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->r()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->a_(Ljava/lang/String;)V

    invoke-direct {p0}, Lpmsj/work/main/k;->as()V

    invoke-direct {p0}, Lpmsj/work/main/k;->aq()V

    return-void
.end method

.method public final j()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/k;->aF:Lpmsj/work/b/p;

    invoke-virtual {v0}, Lpmsj/work/b/p;->b()V

    return-void
.end method

.method public final k()V
    .locals 1

    iget-object v0, p0, Lpmsj/work/main/k;->aF:Lpmsj/work/b/p;

    invoke-virtual {v0}, Lpmsj/work/b/p;->e()V

    return-void
.end method

.method protected final l()Z
    .locals 12

    const/4 v5, 0x3

    const/16 v4, 0xc

    const/4 v11, 0x2

    const/4 v10, 0x1

    const/4 v9, 0x0

    new-array v0, v4, [I

    fill-array-data v0, :array_0

    new-array v1, v4, [Ljava/lang/String;

    const-string v2, "\u89d2\u8272\u4fe1\u606f"

    aput-object v2, v1, v9

    const-string v2, "\u7269\u54c1\u80cc\u5305"

    aput-object v2, v1, v10

    const-string v2, "\u90ae\u7bb1"

    aput-object v2, v1, v11

    sget-object v2, Lpmsj/work/a/c;->aJ:[Ljava/lang/String;

    aget-object v2, v2, v9

    aput-object v2, v1, v5

    const/4 v2, 0x4

    const-string v3, "\u7cfb\u7edf\u8bbe\u7f6e"

    aput-object v3, v1, v2

    const/4 v2, 0x5

    const-string v3, "\u804a\u5929"

    aput-object v3, v1, v2

    const/4 v2, 0x6

    const-string v3, "\u5ba0\u7269\u5217\u8868"

    aput-object v3, v1, v2

    const/4 v2, 0x7

    const-string v3, "\u4ed9\u6676\u5546\u5e97"

    aput-object v3, v1, v2

    const/16 v2, 0x8

    const-string v3, "\u961f\u4f0d"

    aput-object v3, v1, v2

    const/16 v2, 0x9

    const-string v3, "\u5e2e\u6d3e"

    aput-object v3, v1, v2

    const/16 v2, 0xa

    const-string v3, "\u6392\u884c"

    aput-object v3, v1, v2

    const/16 v2, 0xb

    const-string v3, "\u793e\u4ea4\u5173\u7cfb"

    aput-object v3, v1, v2

    new-array v2, v4, [Ljava/lang/String;

    const-string v3, "\u4eba\u7269"

    aput-object v3, v2, v9

    const-string v3, "\u80cc\u5305"

    aput-object v3, v2, v10

    const-string v3, "\u90ae\u7bb1"

    aput-object v3, v2, v11

    const-string v3, "\u4efb\u52a1"

    aput-object v3, v2, v5

    const/4 v3, 0x4

    const-string v4, "\u670d\u52a1"

    aput-object v4, v2, v3

    const/4 v3, 0x5

    const-string v4, "\u804a\u5929"

    aput-object v4, v2, v3

    const/4 v3, 0x6

    const-string v4, "\u5ba0\u7269"

    aput-object v4, v2, v3

    const/4 v3, 0x7

    const-string v4, "\u5546\u57ce"

    aput-object v4, v2, v3

    const/16 v3, 0x8

    const-string v4, "\u961f\u4f0d"

    aput-object v4, v2, v3

    const/16 v3, 0x9

    const-string v4, "\u5e2e\u6d3e"

    aput-object v4, v2, v3

    const/16 v3, 0xa

    const-string v4, "\u6392\u884c"

    aput-object v4, v2, v3

    const/16 v3, 0xb

    const-string v4, "\u793e\u4ea4"

    aput-object v4, v2, v3

    const-string v3, "\u83dc\u5355"

    array-length v4, v0

    new-array v4, v4, [Lpmsj/work/a/i;

    move v5, v9

    :goto_0
    array-length v6, v0

    if-ge v5, v6, :cond_0

    new-instance v6, Lpmsj/work/a/i;

    const v7, 0x220e0a

    aget v8, v0, v5

    invoke-direct {v6, v7, v8}, Lpmsj/work/a/i;-><init>(II)V

    aput-object v6, v4, v5

    add-int/lit8 v5, v5, 0x1

    goto :goto_0

    :cond_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    move v5, v9

    :goto_1
    if-ge v5, v11, :cond_1

    add-int/lit16 v6, v5, 0x17c

    invoke-virtual {v0, v6}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v7

    if-nez v7, :cond_3

    new-instance v7, Lpmsj/work/e/ap;

    invoke-direct {v7}, Lpmsj/work/e/ap;-><init>()V

    invoke-virtual {v0, v6, v7}, Lpmsj/work/d/n;->a(ILpmsj/work/d/c;)V

    if-lez v5, :cond_2

    const/16 v5, 0x17c

    invoke-virtual {v0, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    :goto_2
    invoke-virtual {v7, v0}, Lpmsj/work/e/ap;->a(Lpmsj/work/d/c;)V

    invoke-virtual {v7, v1, v2, v4, v3}, Lpmsj/work/e/ap;->a([Ljava/lang/String;[Ljava/lang/String;[Lpmsj/work/a/i;Ljava/lang/String;)V

    :cond_1
    return v10

    :cond_2
    move-object v0, p0

    goto :goto_2

    :cond_3
    invoke-virtual {v0, v6}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v6

    invoke-virtual {v6, v9}, Lpmsj/work/d/c;->a(Z)V

    add-int/lit8 v5, v5, 0x1

    goto :goto_1

    nop

    :array_0
    .array-data 4
        0x0
        0x1
        0x2
        0x3
        0x4
        0x5
        0x6
        0x7
        0x8
        0x9
        0xa
        0xb
    .end array-data
.end method

.method protected final m()Z
    .locals 1

    invoke-direct {p0}, Lpmsj/work/main/k;->ar()V

    const/4 v0, 0x1

    return v0
.end method

.method public final n()V
    .locals 0

    invoke-direct {p0}, Lpmsj/work/main/k;->as()V

    invoke-direct {p0}, Lpmsj/work/main/k;->aq()V

    return-void
.end method

.method public final o()V
    .locals 6

    const/4 v5, 0x0

    sget-boolean v0, Lpmsj/work/main/f;->f:Z

    if-nez v0, :cond_1

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    invoke-virtual {v0, v5}, Lpmsj/work/d/g;->a(Z)V

    :cond_0
    return-void

    :cond_1
    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lpmsj/work/d/g;->a(Z)V

    invoke-static {v5}, Lpmsj/work/main/x;->a(B)Lpmsj/work/main/x;

    move-result-object v1

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    invoke-virtual {v0}, Lpmsj/work/d/g;->k()I

    move-result v2

    move v3, v5

    :goto_0
    if-ge v3, v2, :cond_0

    iget-object v0, v1, Lpmsj/work/main/x;->a:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v3, v0, :cond_0

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    invoke-virtual {v0, v3}, Lpmsj/work/d/g;->a(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/a;

    if-nez v0, :cond_2

    new-instance v0, Lpmsj/work/d/a;

    const-string v4, ""

    invoke-direct {v0, v4, v5}, Lpmsj/work/d/a;-><init>(Ljava/lang/String;I)V

    iget-object v4, p0, Lpmsj/work/main/k;->f:Lpmsj/work/a/i;

    invoke-virtual {v0, v4}, Lpmsj/work/d/a;->b(Lpmsj/work/a/i;)V

    iget-object v4, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    invoke-virtual {v4, v0, v3}, Lpmsj/work/d/g;->a(Lpmsj/work/d/b;I)V

    move-object v4, v0

    :goto_1
    iget-object v0, v1, Lpmsj/work/main/x;->a:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/main/r;

    invoke-virtual {v0}, Lpmsj/work/main/r;->b()Lpmsj/work/a/i;

    move-result-object v0

    invoke-virtual {v4, v0}, Lpmsj/work/d/a;->c(Lpmsj/work/a/i;)V

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_0

    :cond_2
    move-object v4, v0

    goto :goto_1
.end method

.method public final p()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/main/k;->U:Lpmsj/work/d/l;

    sget v1, Lpmsj/work/main/k;->c:I

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->t(I)V

    invoke-direct {p0}, Lpmsj/work/main/k;->at()V

    return-void
.end method

.method public final r()I
    .locals 1

    iget v0, p0, Lpmsj/work/main/k;->aL:I

    return v0
.end method

.method public final s()V
    .locals 1

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/main/k;->aK:La/c/q;

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/main/k;->aL:I

    return-void
.end method

.method protected final t()V
    .locals 3

    sget-short v0, Lpmsj/work/main/t;->d:S

    iget v1, p0, Lpmsj/work/main/k;->l:I

    if-eq v0, v1, :cond_0

    sget-short v0, Lpmsj/work/main/t;->d:S

    invoke-virtual {p0, v0}, Lpmsj/work/main/k;->j(I)V

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    sget-short v1, Lpmsj/work/main/t;->d:S

    iget-object v2, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    iget v2, v2, Lpmsj/work/d/b;->l:I

    sub-int/2addr v1, v2

    const/4 v2, 0x2

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    :cond_0
    sget-short v0, Lpmsj/work/main/t;->c:S

    iget v1, p0, Lpmsj/work/main/k;->k:I

    if-eq v0, v1, :cond_1

    sget-short v0, Lpmsj/work/main/t;->c:S

    iput v0, p0, Lpmsj/work/d/b;->k:I

    iget-object v0, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    sget-short v1, Lpmsj/work/main/t;->c:S

    iget-object v2, p0, Lpmsj/work/main/k;->W:Lpmsj/work/d/g;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->i:S

    :cond_1
    return-void
.end method
